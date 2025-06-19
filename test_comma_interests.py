#!/usr/bin/env python3
"""
Test script to verify comma-separated interests functionality
"""

import requests
import json

def test_comma_interests():
    """Test the comma-separated interests flow"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = "test_comma_interests"
    
    print("🧪 Testing Comma-Separated Interests Flow")
    print("=" * 50)
    
    # Test messages for the profile flow up to interests
    test_messages = [
        "Hello",
        "John",
        "Emma", 
        "10",
        "5",
        "soccer, basketball, art",  # Multiple interests with commas
        "",  # Empty message to continue
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
                
                # Check if this is the interests step and show the interests
                if "interests" in data['response'].lower() and "soccer, basketball, art" in message:
                    print(f"🎯 Testing comma-separated interests: {message}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Comma Interests Test Complete!")

if __name__ == "__main__":
    test_comma_interests() 