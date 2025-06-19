#!/usr/bin/env python3
"""
Test script to verify interests step automatically continues
"""

import requests
import json
import time

def test_auto_continue():
    """Test that interests step automatically continues"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = f"test_auto_continue_{int(time.time())}"  # Fresh session ID
    
    print("🧪 Testing Auto-Continue Interests Flow")
    print("=" * 50)
    
    # Test messages for the profile flow up to interests
    test_messages = [
        "Hello",
        "John",
        "Emma", 
        "10",
        "5",
        "soccer, basketball, art",  # Multiple interests - should auto-continue
        "123 Main St, San Francisco, CA",
        "50"
    ]
    
    for i, message in enumerate(test_messages, 1):
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
                print(f"🤖 Response: {data['response'][:100]}...")
                
                # Check if interests step auto-continued
                if "soccer, basketball, art" in message and "Where are you located" in data['response']:
                    print("🎯 SUCCESS: Interests step automatically continued to address!")
                elif "Enter another interest" in data['response']:
                    print("❌ FAILED: Still asking for more interests!")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Auto-Continue Test Complete!")

if __name__ == "__main__":
    test_auto_continue() 