# AuraYouth - Mental Wellness Platform for Youth

A modern, empathetic, and confidential mental wellness platform designed specifica4. **Configure environment**
   Edit `.env` file:
   ```env
   SECRET_KEY=your-secret-key-change-in-production
   PORT=8000
   MONGO_URL=mongodb://localhost:27017
   DATABASE_NAME=aurayouth
   GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key
   ```outh, featuring multimodal AI-powered support with React frontend and FastAPI backend.

## 🚀 Features

### Core Functionality
- **Multimodal Chat Support**: Text, audio, and video analysis for comprehensive emotional support
- **AI-Powered Crisis Detection**: Real-time monitoring and intervention for crisis situations
- **Emotion Analysis**: Advanced sentiment analysis and mood tracking
- **Confidential & Secure**: End-to-end encryption and HIPAA-compliant data handling

### User Experience
- **WHO-Inspired Design**: Professional healthcare interface following WHO design standards
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: WCAG 2.1 compliant with screen reader support
- **Multilingual Support**: Available in multiple languages

### AI Integration
- **Google Gemini AI**: Advanced contextual responses with conversation history (requires API key)
- **Fallback Responses**: Keyword-based empathetic responses when Gemini is unavailable
- **Emotion Detection**: Real-time sentiment analysis and mood tracking
- **Crisis Detection**: Pattern recognition for crisis situations
- **Contextual Responses**: AI-powered empathetic responses with memory
- **Digital Twin Learning**: Personalized responses based on conversation history

### Setup Notes
- **Gemini API**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Model Selection**: The current model is set to 'gemini-pro'. If you encounter model errors, check available models in your Google AI console
- **Fallback Mode**: The system gracefully falls back to keyword-based responses if Gemini is unavailable

### Technical Features
- **Real-time Communication**: WebSocket-based chat with instant responses
- **File Upload Support**: Secure audio/video file processing
- **Authentication System**: JWT-based secure authentication
- **Progress Tracking**: Mood trends and conversation history
- **Conversation Storage**: Persistent chat history for personalized support

## 🛠️ Technology Stack

### Frontend (React)
- **React 18** - Modern JavaScript library for building user interfaces
- **Vite** - Fast build tool and development server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **Lucide React** - Modern icon library
- **CSS Modules** - Component-scoped styling

### Backend (FastAPI)
- **FastAPI** - Modern Python web framework
- **WebSocket** - Real-time communication
- **JWT** - JSON Web Token authentication
- **SQLAlchemy** - Database ORM
- **Google Generative AI** - Advanced AI-powered chat responses
- **Librosa** - Audio processing
- **OpenCV** - Video processing

## 📁 Project Structure

```
AuraYouth/
├── frontend/                    # React frontend application
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # Reusable React components
│   │   │   ├── Header.jsx       # Navigation header
│   │   │   ├── Footer.jsx       # Site footer
│   │   │   └── *.css            # Component styles
│   │   ├── contexts/            # React contexts
│   │   │   └── AuthContext.jsx  # Authentication state management
│   │   ├── pages/               # Page components
│   │   │   ├── Home.jsx         # Landing page
│   │   │   ├── Login.jsx        # Authentication page
│   │   │   ├── Chat.jsx         # Multimodal chat interface
│   │   │   ├── Profile.jsx      # User profile and settings
│   │   │   ├── CrisisSupport.jsx # Crisis resources and hotlines
│   │   │   └── *.css            # Page-specific styles
│   │   ├── App.jsx              # Main application component
│   │   ├── App.css              # Global styles
│   │   └── main.jsx             # Application entry point
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.js           # Vite configuration
│   └── index.html               # HTML template
├── main.py                      # FastAPI backend application
├── index.html                   # Legacy HTML frontend (deprecated)
├── ai/                          # AI components
│   ├── chatbot.py               # AI conversation logic
│   ├── emotion_recognition.py   # Multimodal emotion analysis
│   └── digital_twin.py          # User profiling
├── auth/                        # Authentication
│   └── security.py               # JWT authentication
├── database/                    # Database connections
│   └── connection.py             # Database setup
├── uploads/                     # File upload directory
│   ├── audio/                   # Audio file storage
│   └── video/                   # Video file storage
├── pyproject.toml               # Backend dependencies
├── README.md                    # This documentation
└── .env                         # Configuration
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm (for frontend)
- Python 3.8+ and uv package manager (for backend)
- MongoDB (optional - works in demo mode without it)

### Frontend Setup (React)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:5173`

### Backend Setup (FastAPI)

1. **Navigate to root directory**
   ```bash
   cd ..
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   Edit `.env` file:
   ```env
   SECRET_KEY=your-secret-key-change-in-production
   PORT=8000
   MONGO_URL=mongodb://localhost:27017
   DATABASE_NAME=aurayouth
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Start the backend server**
   ```bash
   uv run python main.py
   ```

5. **API will be available at**
   `http://localhost:8000`

## 🔧 Available Scripts

### Frontend Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Backend Scripts
- `uv run python main.py` - Start development server
- `uv run python test_multimodal.py` - Run multimodal tests
- `uv run python demo_multimodal.py` - Run interactive demo

## 🎨 Design System

### Color Palette (WHO-Inspired)
- **Primary**: `#007acc` (WHO Blue)
- **Secondary**: `#2c3e50` (Dark Blue-Gray)
- **Accent**: `#e74c3c` (Crisis Red)
- **Background**: `#f5f7fa` (Light Gray)
- **Success**: `#27ae60` (Green)
- **Warning**: `#f39c12` (Orange)

### Typography
- **Font Family**: System fonts with fallbacks
- **Headings**: 600 font-weight, 1.2 line-height
- **Body Text**: 400 font-weight, 1.6 line-height
- **Scale**: Modular scale based on 1rem = 16px

### Components
- **Buttons**: Rounded corners, hover effects, focus states
- **Cards**: Shadow effects, hover animations
- **Forms**: Clear labels, validation states, accessibility
- **Navigation**: Clean, intuitive, responsive

## 🔐 Authentication

### JWT-Based Authentication
1. **Login**: Users authenticate with username/password
2. **Token Storage**: JWT stored securely in localStorage
3. **Auto-refresh**: Automatic token refresh on expiration
4. **Protected Routes**: Certain pages require authentication

### Demo Credentials
- **Username**: demo_user
- **Password**: demo_pass

## 💬 Chat Features

### Multimodal Support
- **Text Chat**: Standard text-based conversation
- **Audio Upload**: Voice message analysis using Librosa
- **Video Upload**: Facial expression analysis using OpenCV
- **File Processing**: Secure, server-side processing

### AI Integration
- **Emotion Detection**: Real-time sentiment analysis
- **Crisis Detection**: Pattern recognition for crisis situations
- **Contextual Responses**: AI-powered empathetic responses
- **Cultural Sensitivity**: Culturally appropriate responses

### Safety Features
- **Crisis Alerts**: Automatic detection and intervention
- **Emergency Contacts**: Quick access to crisis resources
- **Moderation**: Content filtering and safety checks

## 🌐 Crisis Support

### International Resources
- **Hotlines**: Country-specific crisis hotlines (US, UK, Canada, etc.)
- **Emergency Services**: Local emergency contact information
- **Support Organizations**: Mental health organizations and resources

### Coping Strategies
- **Breathing Exercises**: Guided breathing techniques
- **Grounding Techniques**: 5-4-3-2-1 grounding method
- **Self-Care Resources**: Healthy coping mechanisms

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## ♿ Accessibility

- **WCAG 2.1 AA Compliance**: Meets accessibility standards
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: ARIA labels and semantic HTML
- **Color Contrast**: High contrast ratios for readability
- **Focus Management**: Clear focus indicators

## 🔒 Security

### Data Protection
- **End-to-end Encryption**: All communications encrypted
- **Secure Storage**: Sensitive data encrypted at rest
- **GDPR Compliance**: European data protection standards
- **HIPAA Considerations**: Healthcare data protection

### Privacy Features
- **Anonymous Usage**: Option for anonymous interactions
- **Data Minimization**: Only necessary data collection
- **User Control**: Data export and deletion options
- **Consent Management**: Clear privacy consent

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
```

### Backend Testing
```bash
uv run python test_multimodal.py
```

### Manual Testing
1. **Web Interface**: Open `http://localhost:5173`
2. **Login**: Use demo credentials
3. **Test Chat**: Send messages and upload files
4. **Test Crisis Support**: Access crisis resources
5. **Test Profile**: View user statistics and settings

## 📊 API Documentation

### Authentication Endpoints

#### POST /auth/login
```json
{
  "username": "demo_user",
  "password": "demo_pass"
}
```

#### GET /auth/me
Get current user information (requires authentication).

### Chat Endpoints

#### POST /chat
Send a text message to the AI chatbot.

#### POST /chat/multimodal
Send a multimodal message with optional audio/video files.

**Request:**
```json
{
  "message": "I'm feeling anxious",
  "user_id": "demo_user",
  "audio_file": "/uploads/audio/recording.wav",
  "video_file": "/uploads/video/video.mp4"
}
```

### File Upload Endpoints

#### POST /upload/audio
Upload audio file (WAV, MP3, M4A, FLAC)

#### POST /upload/video
Upload video file (MP4, AVI, MOV, MKV)

## 🚀 Deployment

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy the dist/ folder to your hosting service
```

### Backend Deployment
```bash
# Using Docker
docker build -t aurayouth-backend .
docker run -p 8000:8000 aurayouth-backend
```

### Environment Variables
```env
# Frontend
VITE_API_URL=http://localhost:8000

# Backend
SECRET_KEY=your-secret-key
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- **JavaScript**: ESLint with React rules
- **Python**: Black formatter, Flake8 linting
- **CSS**: CSS Modules with BEM methodology
- **Git**: Conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **World Health Organization** for design inspiration and mental health guidelines
- **OpenAI** for AI-powered chat capabilities
- **React Community** for excellent documentation and tools
- **Mental Health Organizations** for crisis resources and support information

## 📞 Support

For support, please contact:
- **Email**: support@aurayouth.org
- **Crisis Hotline**: Available 24/7 through the app
- **Documentation**: [Full API Documentation](docs/api.md)

---

**Remember**: If you're experiencing a mental health crisis, please reach out to emergency services or a crisis hotline immediately. This platform is designed to support, not replace, professional mental health care.
