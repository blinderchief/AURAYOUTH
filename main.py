from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
import asyncio
from ai.chatbot import Chatbot
from ai.emotion_recognition import EmotionRecognition
from ai.digital_twin import DigitalTwin
from database.connection import get_database, connect_to_database, close_database_connection
from auth.security import authenticate_user, create_access_token, get_current_active_user, get_current_user, fake_users_db, Token
import os
import shutil
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import timedelta

load_dotenv()

# Initialize AI components
chatbot = Chatbot()
emotion_recog = EmotionRecognition()
digital_twin = DigitalTwin()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_database()
    yield
    # Shutdown
    await close_database_connection()

app = FastAPI(title="AuraYouth API", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Security
security = HTTPBearer()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    context: Optional[dict] = None

class MultimodalChatRequest(BaseModel):
    message: str
    user_id: str
    context: Optional[dict] = None
    audio_file: Optional[str] = None  # Path to uploaded audio file
    video_file: Optional[str] = None  # Path to uploaded video file

class ChatResponse(BaseModel):
    response: str
    emotion: str
    confidence: float
    crisis_detected: Optional[bool] = False
    crisis_type: Optional[str] = None

class UserProfile(BaseModel):
    user_id: str
    age: int
    preferences: dict
    history: List[dict]

class UserLogin(BaseModel):
    username: str
    password: str

# API Endpoints
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/auth/login", response_model=Token)
async def login(form_data: UserLogin):
    """Authenticate user and return JWT token."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def read_users_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information."""
    token = credentials.credentials
    user = await get_current_active_user(await get_current_user(token))
    return {"username": user.username, "email": user.email, "full_name": user.full_name}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Protected chat endpoint that requires authentication."""
    try:
        # Verify token
        token = credentials.credentials
        current_user = await get_current_active_user(await get_current_user(token))
        
        # Analyze emotion
        emotion = emotion_recog.analyze_text(request.message)
        
        # Check for crisis situation
        crisis_detected = emotion.get("crisis_detected", False)
        crisis_type = emotion.get("crisis_type", None)
        
        # Get chatbot response
        response = await chatbot.generate_response(
            request.message, 
            request.user_id, 
            emotion,
            request.context
        )
        
        # Update digital twin (only if database is available)
        if get_database() is not None:
            await digital_twin.update_profile(request.user_id, {
                "message": request.message,
                "emotion": emotion["label"],
                "response": response,
                "crisis_detected": crisis_detected,
                "crisis_type": crisis_type
            })
        
        # Add crisis flag to response if detected
        if crisis_detected:
            return ChatResponse(
                response=response,
                emotion="crisis",
                confidence=emotion["confidence"],
                crisis_detected=True,
                crisis_type=crisis_type
            )
        
        return ChatResponse(
            response=response,
            emotion=emotion["label"],
            confidence=emotion["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: dict = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.user_connections:
            websocket = self.user_connections[user_id]
            await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat."""
    print(f"WebSocket connection established for user: {user_id}")
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received message from {user_id}: {data}")
            message_data = json.loads(data)
            
            # Analyze emotion
            emotion = emotion_recog.analyze_text(message_data["message"])
            
            # Get AI response
            crisis_type = chatbot._detect_crisis(message_data["message"])
            crisis_detected = crisis_type is not None
            response = await chatbot.generate_response(
                message_data["message"],
                user_id,
                emotion,
                message_data.get("context", [])
            )
            
            # Prepare response
            import time
            bot_message_id = f"{int(time.time() * 1000)}-{hash(response) % 10000}"
            response_data = {
                "id": bot_message_id,
                "type": "bot",
                "content": response,
                "emotion": emotion["label"],
                "confidence": emotion["confidence"],
                "crisis_detected": crisis_detected,
                "crisis_type": crisis_type,
                "timestamp": str(asyncio.get_event_loop().time())
            }
            
            print(f"Sending response to {user_id}: {response_data}")
            # Send response back to client
            await manager.send_personal_message(json.dumps(response_data), user_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        print(f"Client {user_id} disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)

@app.post("/profile")
async def create_profile(profile: UserProfile):
    # For demo, store in memory
    return {"user_id": profile.user_id, "message": "Profile created (demo mode)"}

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    # For demo, return mock data
    return {
        "user_id": user_id,
        "age": 18,
        "preferences": {"theme": "light"},
        "history": []
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "features": ["multimodal", "crisis_detection"]}

@app.post("/upload/audio")
async def upload_audio(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Upload audio file for emotion analysis."""
    try:
        # Verify token
        token = credentials.credentials
        current_user = await get_current_active_user(await get_current_user(token))
        
        # Validate file type
        if not file.filename or not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
            raise HTTPException(status_code=400, detail="Unsupported audio format")
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/audio"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with unique name
        file_path = f"{upload_dir}/{current_user.username}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"file_path": file_path, "message": "Audio file uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/video")
async def upload_video(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Upload video file for emotion analysis."""
    try:
        # Verify token
        token = credentials.credentials
        current_user = await get_current_active_user(await get_current_user(token))
        
        # Validate file type
        if not file.filename or not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            raise HTTPException(status_code=400, detail="Unsupported video format")
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/video"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with unique name
        file_path = f"{upload_dir}/{current_user.username}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"file_path": file_path, "message": "Video file uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/multimodal", response_model=ChatResponse)
async def multimodal_chat_endpoint(
    request: MultimodalChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Protected multimodal chat endpoint with audio/video analysis."""
    try:
        # Verify token
        token = credentials.credentials
        current_user = await get_current_active_user(await get_current_user(token))
        
        # Perform multimodal emotion analysis
        emotion = emotion_recog.analyze_multimodal(
            text=request.message,
            audio_path=request.audio_file,
            image_path=request.video_file
        )
        
        # Check for crisis situation
        crisis_detected = emotion.get("crisis_detected", False)
        crisis_type = emotion.get("crisis_type", None)
        
        # Get chatbot response with multimodal context
        response = await chatbot.generate_response(
            request.message, 
            request.user_id, 
            emotion,
            request.context
        )
        
        # Update digital twin (only if database is available)
        if get_database() is not None:
            await digital_twin.update_profile(request.user_id, {
                "message": request.message,
                "emotion": emotion.get("multimodal_emotion", emotion.get("label", "neutral")),
                "response": response,
                "crisis_detected": crisis_detected,
                "crisis_type": crisis_type,
                "multimodal": True,
                "audio_analysis": emotion.get("audio_analysis"),
                "video_analysis": emotion.get("video_analysis")
            })
        
        # Return response with multimodal emotion data
        final_emotion = emotion.get("final_emotion", emotion.get("multimodal_emotion", emotion.get("label", "neutral")))
        final_confidence = emotion.get("final_confidence", emotion.get("multimodal_confidence", emotion.get("confidence", 0.5)))
        
        if crisis_detected:
            return ChatResponse(
                response=response,
                emotion="crisis",
                confidence=final_confidence,
                crisis_detected=True,
                crisis_type=crisis_type
            )
        
        return ChatResponse(
            response=response,
            emotion=final_emotion,
            confidence=final_confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
