from typing import Tuple, Optional
import googlemaps
from config import settings
import logging

logger = logging.getLogger(__name__)

class DistanceCalculator:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=settings.google_maps_api_key)

    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude coordinates for an address using Google Maps Geocoding API.
        """
        try:
            geocode_result = self.gmaps.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
            return None
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