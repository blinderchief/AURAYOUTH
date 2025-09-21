#!/usr/bin/env python3
"""
Demo script showing how to use AuraYouth multimodal features
"""

import requests
import json
import time
import os

API_BASE = "http://localhost:8000"

def demo_multimodal_chat():
    """Demonstrate multimodal chat functionality"""
    print("🎭 AuraYouth Multimodal Chat Demo")
    print("=" * 50)

    # Step 1: Login
    print("1. Logging in...")
    login_response = requests.post(f"{API_BASE}/auth/login", json={
        "username": "testuser",
        "password": "password"
    })

    if login_response.status_code != 200:
        print("❌ Login failed")
        return

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # Step 2: Test different emotion scenarios
    test_messages = [
        "I'm feeling really happy today!",
        "I'm so stressed about school",
        "I feel anxious about everything",
        "I'm really sad and don't know what to do",
        "I want to end it all, I can't take this anymore"
    ]

    print("\n2. Testing emotion detection...")
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: '{message[:30]}...'")

        # Test regular chat
        response = requests.post(f"{API_BASE}/chat", json={
            "message": message,
            "user_id": "demo_user",
            "context": {}
        }, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"   Regular Chat: {data['emotion']} ({data['confidence']:.2f})")
            if data.get('crisis_detected'):
                print(f"   🚨 CRISIS DETECTED: {data['crisis_type']}")

        # Test multimodal chat (without files)
        response = requests.post(f"{API_BASE}/chat/multimodal", json={
            "message": message,
            "user_id": "demo_user",
            "context": {},
            "audio_file": None,
            "video_file": None
        }, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"   Multimodal: {data['emotion']} ({data['confidence']:.2f})")
            if data.get('crisis_detected'):
                print(f"   🚨 CRISIS DETECTED: {data['crisis_type']}")

        time.sleep(0.5)  # Brief pause between requests

    print("\n3. Demo completed!")
    print("\n📁 To test file uploads:")
    print("   - Use the web interface at http://localhost:8000")
    print("   - Login with testuser/password")
    print("   - Upload audio/video files using the buttons")
    print("   - Enable 'Multimodal Analysis' checkbox")
    print("   - Send messages to see enhanced emotion detection")

    print("\n🎯 Key Features:")
    print("   ✅ Crisis Detection - Automatic emergency response")
    print("   ✅ Multimodal Analysis - Text + Audio + Video")
    print("   ✅ Real-time Processing - Fast emotion analysis")
    print("   ✅ Secure Authentication - JWT-based security")
    print("   ✅ File Upload Support - Audio/Video processing")

if __name__ == "__main__":
    demo_multimodal_chat()