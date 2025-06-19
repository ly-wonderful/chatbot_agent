#!/usr/bin/env python3
"""
Test script to verify categories are displayed in interests step
"""

import requests
import json
import time

def test_categories_display():
    """Test that categories are displayed when reaching interests step"""
    base_url = "http://localhost:8001/api/v1/chat"
    session_id = f"test_display_{int(time.time())}"
    
    print("🧪 Testing Categories Display in Interests Step")
    print("=" * 50)
    
    # Test messages to get to interests step
    test_messages = [
        "Hello",
        "John",
        "Emma", 
        "10",
        "5"
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
                
                # Check if this is the interests step
                if "interests" in data['response'].lower():
                    print("🎯 SUCCESS: Reached interests step!")
                    
                    # Check if categories are displayed
                    if "popular camp categories" in data['response']:
                        print("🎯 SUCCESS: Categories are being displayed!")
                        print("📋 Categories shown:")
                        # Extract and display the categories
                        lines = data['response'].split('\n')
                        for line in lines:
                            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                                print(f"   {line.strip()}")
                    else:
                        print("❌ FAILED: Categories not displayed")
                
                print(f"🤖 Response preview: {data['response'][:100]}...")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("✅ Categories Display Test Complete!")

if __name__ == "__main__":
    test_categories_display() 