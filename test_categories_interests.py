#!/usr/bin/env python3
"""
Test script to verify interests step with category selection
"""

import requests
import json
import time

def test_categories_interests():
    """Test the interests step with category selection"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = f"test_categories_{int(time.time())}"
    
    print("🧪 Testing Interests with Category Selection")
    print("=" * 50)
    
    # Test messages for the profile flow up to interests
    test_messages = [
        "Hello",
        "John",
        "Emma", 
        "10",
        "5",
        "1, 3, 5",  # Select categories by number
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
                print(f"🤖 Response: {data['response'][:300]}...")
                
                # Check if interests step shows categories
                if "popular camp categories" in data['response']:
                    print("🎯 SUCCESS: Categories are being displayed!")
                
                # Check if interests step auto-continued
                if "1, 3, 5" in message and "Where are you located" in data['response']:
                    print("🎯 SUCCESS: Interests step automatically continued to address!")
                
                # Check if profile step is correct
                if hasattr(data, 'profile_step'):
                    print(f"🔍 Profile step: {data.get('profile_step', 'N/A')}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("✅ Categories Interests Test Complete!")

if __name__ == "__main__":
    test_categories_interests() 