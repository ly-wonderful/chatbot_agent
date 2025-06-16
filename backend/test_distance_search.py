import asyncio
from database.supabase_client import supabase_client
from models.schemas import CampSearchFilters
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def search_camps_by_address():
    """Interactive function to search camps based on user's home address"""
    
    print("\n🏠 Camp Search by Distance")
    print("------------------------")
    
    # Get user's home address
    home_address = input("\nEnter your home address (e.g., '123 Main St, City, State'): ").strip()
    if not home_address:
        print("❌ No address provided. Using default San Francisco address.")
        home_address = "123 Market St, San Francisco, CA"
    
    # Get maximum distance
    while True:
        try:
            max_distance = input("\nEnter maximum driving distance in miles (default: 50): ").strip()
            max_distance = float(max_distance) if max_distance else 50
            if max_distance <= 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Get optional category filter
    category = input("\nEnter camp category to filter by (optional, press Enter to skip): ").strip()
    
    print("\n🔍 Searching for camps...")
    
    try:
        # Create search filters
        filters = CampSearchFilters(
            address=home_address,
            max_driving_distance_miles=max_distance
        )
        
        if category:
            filters.category = category
        
        # Search for camps
        result = await supabase_client.search_camps(filters)
        camps = result["camps"]
        selected_location = result["selected_location"]
        
        if not camps:
            print(f"\n❌ No camps found within {max_distance} miles of your location.")
            if category:
                print(f"Try removing the '{category}' category filter or increasing the distance.")
            return
        
        # Display results
        print(f"\n✅ Found {len(camps)} camps within {max_distance} miles of your location")
        if selected_location and selected_location != home_address:
            print(f"📍 Using location: {selected_location}")
        if category:
            print(f"Filtered by category: {category}")
        
        print("\n📋 Camp Details:")
        print("----------------")
        
        for i, camp in enumerate(camps, 1):
            print(f"\n{i}. {camp.get('camp_name', 'Unnamed Camp')}")
            
            # Get organization name
            org = camp.get('organizations', {})
            if org:
                print(f"   Organization: {org.get('name', 'Unknown')}")
            
            # Get location and distance
            for session in camp.get('camp_sessions', []):
                location = session.get('locations')
                if location:
                    print(f"   Location: {location.get('city', '')}, {location.get('state', '')}")
                    print(f"   Address: {location.get('formatted_address', 'No address available')}")
                    break
            
            # Get price if available
            if camp.get('price'):
                print(f"   Price: ${camp['price']}/week")
            
            # Get grade range if available
            if camp.get('min_grade') is not None and camp.get('max_grade') is not None:
                print(f"   Grades: {camp['min_grade']}-{camp['max_grade']}")
            
            # Get description if available
            if camp.get('description'):
                desc = camp['description'][:150] + "..." if len(camp['description']) > 150 else camp['description']
                print(f"   Description: {desc}")
            
            print("   " + "-" * 40)
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"   Total camps found: {len(camps)}")
        print(f"   Search radius: {max_distance} miles")
        print(f"   From address: {selected_location or home_address}")
        
    except Exception as e:
        print(f"\n❌ Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(search_camps_by_address()) 