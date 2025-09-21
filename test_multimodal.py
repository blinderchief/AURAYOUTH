#!/usr/bin/env python3
"""
Test script for AuraYouth multimodal features
"""

import requests
import json
import os
from pathlib import Path

# Server configuration
API_BASE = "http://localhost:8000"

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print("❌ Server health check failed")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def test_login():
    """Test user authentication"""
    try:
        response = requests.post(f"{API_BASE}/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            return data["access_token"]
        else:
            print("❌ Login failed")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_text_chat(token):
    """Test basic text chat"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_BASE}/chat", json={
            "message": "I'm feeling happy today",
            "user_id": "test_user",
            "context": {}
        }, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("✅ Text chat successful")
            print(f"   Response: {data['response'][:50]}...")
            print(f"   Emotion: {data['emotion']} (confidence: {data['confidence']:.2f})")
            return True
        else:
            print(f"❌ Text chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text chat error: {e}")
        return False

def test_crisis_detection(token):
    """Test crisis detection"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_BASE}/chat", json={
            "message": "I want to end it all",
            "user_id": "test_user",
            "context": {}
        }, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("crisis_detected"):
                print("✅ Crisis detection working")
                print(f"   Crisis type: {data['crisis_type']}")
                return True
            else:
                print("❌ Crisis detection failed")
                return False
        else:
            print(f"❌ Crisis test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Crisis test error: {e}")
        return False

def test_multimodal_chat(token):
    """Test multimodal chat (without actual files)"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_BASE}/chat/multimodal", json={
            "message": "I'm feeling anxious",
            "user_id": "test_user",
            "context": {},
            "audio_file": None,
            "video_file": None
        }, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("✅ Multimodal chat endpoint working")
            print(f"   Response: {data['response'][:50]}...")
            return True
        else:
            print(f"❌ Multimodal chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Multimodal chat error: {e}")
        return False

def main():
    print("🧪 Testing AuraYouth Multimodal Features")
    print("=" * 50)

    # Test server health
    if not test_server_health():
        print("❌ Server not running. Please start the server first.")
        return

    # Test authentication
    token = test_login()
    if not token:
        print("❌ Authentication failed. Cannot continue testing.")
        return

    print()

    # Test basic features
    print("Testing Basic Features:")
    test_text_chat(token)
    test_crisis_detection(token)

    print()

    # Test multimodal features
    print("Testing Multimodal Features:")
    test_multimodal_chat(token)

    print()
    print("🎉 Testing completed!")
    print("Note: File upload testing requires actual audio/video files.")
    print("You can test file uploads manually through the web interface.")

if __name__ == "__main__":
    main()