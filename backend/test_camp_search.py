import asyncio
from database.supabase_client import supabase_client
from models.schemas import CampSearchFilters

async def test_camp_search():

    
    print("🔍 Testing camp searches...")
    

    try:
        filters = CampSearchFilters()
        all_camps = await supabase_client.search_camps(filters)
        print(f"✅ Found {len(all_camps)} total camps with no filters")
        
        if all_camps:
            first_camp = all_camps[0]
            print(f"📋 Sample camp: {first_camp.get('camp_name', 'No name')}")
            print(f"🏢 Organization: {first_camp.get('organizations', {}).get('name', 'No org')}")
            print(f"💰 Price: ${first_camp.get('price', 'No price')}")
        
    except Exception as e:
        print(f"❌ Error searching all camps: {e}")
    

    try:
        filters = CampSearchFilters(category="soccer")
        soccer_camps = await supabase_client.search_camps(filters)
        print(f"⚽ Found {len(soccer_camps)} soccer camps")
        
    except Exception as e:
        print(f"❌ Error searching soccer camps: {e}")
    

    try:
        categories = await supabase_client.get_all_categories()
        print(f"📂 Available categories:")
        for cat in categories[:5]:
            print(f"   - {cat.get('name', 'No name')}")
    except Exception as e:
        print(f"❌ Error getting categories: {e}")

if __name__ == "__main__":
    asyncio.run(test_camp_search())
