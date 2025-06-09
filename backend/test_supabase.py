import asyncio
from database.supabase_client import supabase_client

async def test_supabase_connection():
    """Test if Supabase connection works"""
    try:
        # Test basic connection
        organizations = await supabase_client.get_organizations()
        print(f"✅ Supabase connected! Found {len(organizations)} organizations")
        
        categories = await supabase_client.get_all_categories()
        print(f"✅ Found {len(categories)} categories")
        
        locations = await supabase_client.get_all_locations()
        print(f"✅ Found {len(locations)} locations")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_supabase_connection())
