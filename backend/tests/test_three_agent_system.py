import asyncio
import logging
from app.agents.camp_agent_dynamic import camp_agent
from app.models.schemas import UserProfile

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_three_agent_system():
    """Test the three-agent camp search system"""
    print("🧪 Testing Three-Agent Camp Search System")
    print("=" * 50)
    
    # Test session ID
    session_id = "test_session_001"
    
    # Test messages to simulate a complete conversation
    test_messages = [
        "Hello, I need help finding a summer camp for my child",
        "John",
        "Emma",
        "10",
        "5",
        "soccer",
        "",
        "3991 Porter Ln, Prosper, Tx",
        "20",
        "continue",  # Trigger SQL generation
        "search",    # Trigger database search
        "format"     # Trigger table formatting
    ]
    
    print("📝 Starting profile collection...")
    
    state = None
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Step {i}: {message} ---")
        try:
            state = await camp_agent.process_message(message, session_id, state)
            print(f"🤖 Response: {state.get('final_response')}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Error at step {i}: {e}")
            break
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

async def test_with_existing_profile():
    """Test the system with a pre-existing profile"""
    print("\n🧪 Testing with Pre-existing Profile")
    print("=" * 50)
    
    session_id = "test_session_002"
    
    # Create a complete profile
    profile = UserProfile(
        name="Sarah",
        child_name="Alex",
        child_age=12,
        child_grade=7,
        interests=["basketball", "art", "science"],
        address="456 Oak Ave, Los Angeles, CA",
        max_distance_miles=30
    )
    
    print(f"👤 Profile: {profile.name} - {profile.child_name} (Age: {profile.child_age}, Grade: {profile.child_grade})")
    print(f"📍 Location: {profile.address}")
    print(f"🎯 Interests: {', '.join(profile.interests)}")
    print(f"🚗 Max Distance: {profile.max_distance_miles} miles")
    
    # Test message that should trigger search
    message = "Find camps for Alex"
    
    try:
        # Initialize state with the complete profile
        state = {
            "session_id": session_id,
            "messages": [],
            "current_intent": None,
            "last_search_results": None,
            "search_filters": None,
            "final_response": None,
            "needs_profile": False,  # Profile is complete
            "profile": profile,
            "profile_step": None  # Profile collection is complete
        }
        
        response = await camp_agent.process_message(message, session_id, state)
        print(f"\n🤖 Response: {response.get('final_response')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Pre-existing profile test completed!")

async def test_error_handling():
    """Test error handling in the system"""
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    session_id = "test_session_003"
    
    # Test with invalid input
    invalid_messages = [
        "Hello",
        "John",
        "Emma",
        "invalid_age",  # Invalid age
        "5",
        "soccer",
        "",
        "123 Main St, San Francisco, CA",
        "invalid_distance"  # Invalid distance
    ]
    
    state = None
    for i, message in enumerate(invalid_messages, 1):
        print(f"\n--- Step {i}: {message} ---")
        
        try:
            state = await camp_agent.process_message(message, session_id, state)
            print(f"🤖 Response: {state.get('final_response')}")
            
        except Exception as e:
            print(f"❌ Error at step {i}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Error handling test completed!")

async def main():
    """Run all tests"""
    print("🚀 Starting Three-Agent System Tests")
    print("=" * 60)
    
    # Test 1: Complete profile collection and search
    await test_three_agent_system()
    
    # Test 2: Pre-existing profile
    await test_with_existing_profile()
    
    # Test 3: Error handling
    await test_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 