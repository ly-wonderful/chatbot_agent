import asyncio
from app.database.supabase_client import supabase_client
from app.models.schemas import CampSearchFilters
from scripts.collect_user_profile import collect_user_profile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def search_camps_with_profile():
    """Search camps using user profile information"""
    
    # First collect user profile
    profile = await collect_user_profile()
    
    print("\n🔍 Searching for camps based on your profile...")
    
    try:
        # Create search filters from profile
        filters = CampSearchFilters(
            address=profile.address,
            max_driving_distance_miles=profile.max_distance_miles,
            min_grade=profile.child_grade,
            max_grade=profile.child_grade
        )
        
        # Add category filter if preferred categories exist
        if profile.preferred_categories:
            filters.category = profile.preferred_categories[0]  # Use first preferred category
        
        # Search for camps
        result = await supabase_client.search_camps(filters)
        camps = result["camps"]
        selected_location = result["selected_location"]
        
        if not camps:
            print(f"\n❌ No camps found within {profile.max_distance_miles} miles of your location.")
            if profile.preferred_categories:
                print(f"Try removing the '{profile.preferred_categories[0]}' category filter or increasing the distance.")
            return
        
        # Display results
        print(f"\n✅ Found {len(camps)} camps within {profile.max_distance_miles} miles of your location")
        if selected_location and selected_location != profile.address:
            print(f"📍 Using location: {selected_location}")
        if profile.preferred_categories:
            print(f"Filtered by category: {profile.preferred_categories[0]}")
        
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
        print(f"   Search radius: {profile.max_distance_miles} miles")
        print(f"   From address: {selected_location or profile.address}")
        print(f"   For child: {profile.child_name} (Grade {profile.child_grade})")
        
    except Exception as e:
        print(f"\n❌ Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(search_camps_with_profile()) 