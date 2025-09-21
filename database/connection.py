try:
    from motor.motor_asyncio import AsyncIOMotorClient
    MOTOR_AVAILABLE = True
except ImportError:
    MOTOR_AVAILABLE = False
    print("Motor not available - running in demo mode")

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "aurayouth")

client = None
database = None

async def connect_to_database():
    global client, database
    if not MOTOR_AVAILABLE:
        print("Running in demo mode without database")
        database = None
        return
        
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        database = client[DATABASE_NAME]
        # Test the connection
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {DATABASE_NAME}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        print("Running in demo mode without database")
        database = None

async def close_database_connection():
    global client
    if client and MOTOR_AVAILABLE:
        client.close()
        print("Database connection closed")

def get_database():
    return database