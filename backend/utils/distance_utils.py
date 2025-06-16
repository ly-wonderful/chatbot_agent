from typing import Tuple, Optional, List, Dict
import googlemaps
from config import settings
import logging

logger = logging.getLogger(__name__)

class DistanceCalculator:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=settings.google_maps_api_key)

    def get_coordinates(self, address: str) -> Optional[Tuple[float, float, str]]:
        """
        Get latitude and longitude coordinates for an address using Google Maps Geocoding API.
        Returns a tuple of (latitude, longitude, formatted_address) for the most specific location found.
        """
        try:
            geocode_result = self.gmaps.geocode(address)
            if not geocode_result:
                logger.warning(f"No results found for address: {address}")
                return None

            # Sort results by specificity (more specific addresses first)
            # A more specific address typically has more address components
            sorted_results = sorted(
                geocode_result,
                key=lambda x: len(x.get('address_components', [])),
                reverse=True
            )

            # Get the most specific result
            best_result = sorted_results[0]
            location = best_result['geometry']['location']
            formatted_address = best_result.get('formatted_address', address)

            # Log the selected location
            logger.info(f"Selected location for '{address}': {formatted_address}")
            
            return location['lat'], location['lng'], formatted_address

        except Exception as e:
            logger.error(f"Error geocoding address {address}: {e}")
            return None

    def calculate_driving_distance(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float
    ) -> Optional[float]:
        """
        Calculate driving distance between two points in miles using Google Maps Distance Matrix API.
        """
        try:
            result = self.gmaps.distance_matrix(
                origins=(origin_lat, origin_lng),
                destinations=(dest_lat, dest_lng),
                mode="driving",
                units="imperial"
            )
            
            if result['status'] == 'OK':
                distance = result['rows'][0]['elements'][0]['distance']['value'] / 1609.34  # Convert meters to miles
                return distance
            return None
        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            return None

distance_calculator = DistanceCalculator() 