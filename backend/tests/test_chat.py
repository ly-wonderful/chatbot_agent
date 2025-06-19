#!/usr/bin/env python3

import requests
import json

API_BASE = "http://localhost:8000"

def test_health():

    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_chat(message, session_id=None):

    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id
    
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n🤖 You: {message}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Bot: {data['response']}")
            print(f"Session ID: {data['session_id']}")
            print(f"Context: {data.get('context', {})}")
            return data.get('session_id')
        else:
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"Chat test failed: {e}")
        return None

def interactive_test():

    print("🏕️ Summer Camp Chatbot Test")
    print("=" * 40)
    

    if not test_health():
        print("❌ Backend is not responding. Make sure it's running!")
        return
    
    print("✅ Backend is healthy!")
    session_id = None
    

    test_messages = [
        "Hello!",
        "Find soccer camps for 8 year olds",
        "Show me art camps in California",
        "Tell me more about the first camp",
        "What are the most popular camps?"
    ]
    
    print("\n🧪 Running automated tests...")
    for message in test_messages:
        session_id = test_chat(message, session_id)
        if not session_id:
            break
    

    print("\n💬 Interactive mode (type 'quit' to exit):")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        if user_input:
            session_id = test_chat(user_input, session_id)

if __name__ == "__main__":
    interactive_test()
