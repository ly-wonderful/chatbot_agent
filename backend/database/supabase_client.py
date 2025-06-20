from supabase import create_client, Client
from config import settings
from typing import List, Dict, Optional, Any
from models.schemas import Camp, CampSession, Location, Organization, Category, CampSearchFilters
from utils.distance_utils import distance_calculator
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)
    
    async def search_camps(self, filters: CampSearchFilters) -> Dict[str, Any]:
        try:
            query = self.client.table('camps').select("""
                *,
                organizations(name, email, contact),
                camp_sessions(
                    *,
                    locations(name, city, state, address, formatted_address, latitude, longitude)
                ),
                camp_categories(
                    categories(name)
                )
            """)

            if filters.min_grade is not None:
                query = query.gte('min_grade', filters.min_grade)
            if filters.max_grade is not None:
                query = query.lte('max_grade', filters.max_grade)
            if filters.min_price is not None:
                query = query.gte('price', filters.min_price)
            if filters.max_price is not None:
                query = query.lte('price', filters.max_price)
            
            result = query.execute()
            camps = result.data

            # Filter by location and distance if address is provided
            selected_location = None
            if filters.address and filters.max_driving_distance_miles is not None:
                # Get coordinates for the address
                geocode_result = distance_calculator.get_coordinates(filters.address)
                if not geocode_result:
                    logger.error(f"Could not find coordinates for address: {filters.address}")
                    return {"camps": [], "selected_location": None}
                
                lat, lng, formatted_address = geocode_result
                selected_location = formatted_address
                logger.info(f"Found coordinates for {filters.address}: {lat}, {lng}")
                
                filtered_camps = []
                for camp in camps:
                    for session in camp.get('camp_sessions', []):
                        location = session.get('locations')
                        if location and location.get('latitude') and location.get('longitude'):
                            distance = distance_calculator.calculate_driving_distance(
                                lat, lng,
                                location['latitude'],
                                location['longitude']
                            )
                            if distance is not None and distance <= filters.max_driving_distance_miles:
                                filtered_camps.append(camp)
                                break
                camps = filtered_camps

            # Filter by category
            if filters.category:
                filtered_camps = []
                for camp in camps:
                    for camp_cat in camp.get('camp_categories', []):
                        category = camp_cat.get('categories')
                        if category and filters.category.lower() in category.get('name', '').lower():
                            filtered_camps.append(camp)
                            break
                camps = filtered_camps
            
            return {
                "camps": camps,
                "selected_location": selected_location
            }
            
        except Exception as e:
            logger.error(f"Error searching camps: {e}")
            return {"camps": [], "selected_location": None}
    
    async def get_camp_by_id(self, camp_id: int) -> Optional[Dict[str, Any]]:

        try:
            result = self.client.table('camps').select("""
                *,
                organizations(name, email, contact),
                camp_sessions(
                    *,
                    locations(name, city, state, address, formatted_address, latitude, longitude)
                ),
                camp_categories(
                    categories(name)
                )
            """).eq('id', camp_id).execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting camp by ID {camp_id}: {e}")
            return None
    
    async def get_all_categories(self) -> List[Dict[str, Any]]:

        try:
            result = self.client.table('categories').select('*').execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    async def get_all_locations(self) -> List[Dict[str, Any]]:

        try:
            result = self.client.table('locations').select('*').execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
            return []
    
    async def get_organizations(self) -> List[Dict[str, Any]]:

        try:
            result = self.client.table('organizations').select('*').execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting organizations: {e}")
            return []


supabase_client = SupabaseClient()
