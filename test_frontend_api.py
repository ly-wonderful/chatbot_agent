#!/usr/bin/env python3
"""
Test script to verify the API flow works correctly
"""

import requests
import json
import time

def test_api_flow():
    """Test the complete API flow"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = "test_session_001"
    
    # Test messages
    test_messages = [
        "Hello",
        "John",
        "Emma",
        "10",
        "5",
        "soccer",
        "",
        "123 Main St, San Francisco, CA",
        "50"
    ]
    
    print("🧪 Testing API Flow")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Step {i}: {message} ---")
        
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
                print(f"🤖 Response: {data['response'][:100]}...")
                print(f"🆔 Session: {data['session_id']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("✅ API Flow Test Complete!")

if __name__ == "__main__":
    test_api_flow() 