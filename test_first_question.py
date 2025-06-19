#!/usr/bin/env python3
"""
Test script to check if the first question is being asked twice
"""

import requests
import json

def test_first_question():
    """Test the first question flow"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = "test_first_question"
    
    print("🧪 Testing First Question Flow")
    print("=" * 50)
    
    # Test just the first two messages
    messages = ["Hello", "John"]
    
    for i, message in enumerate(messages, 1):
        print(f"\n--- Step {i}: '{message}' ---")
        
        try:
            response = requests.post(
                base_url,
                json={
                    "message": message,
                    "session_id": session_id
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"🤖 Response: {data['response']}")
                print(f"🆔 Session: {data['session_id']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ First Question Test Complete!")

if __name__ == "__main__":
    test_first_question() 