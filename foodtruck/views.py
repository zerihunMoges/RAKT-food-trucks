from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from .models import FoodTruck
from .serializers import FoodTruckSerializer

class FoodTruckListView(APIView):
    """
    API view for retrieving a list of nearby food trucks based on user's location.

    Parameters:
        - long (float): The longitude of the user's location.
        - lat (float): The latitude of the user's location.
        - searchRadius (float, optional): The search radius in meters. Defaults to 1000 if not provided.
        - status (str, optional): The status of the food trucks to filter by.
        - facilityType (str, optional): The facility type of the food trucks to filter by.

    Returns:
        A JSON response containing the count of nearby food trucks and a list of serialized food truck data.

    Example:
        GET /food-trucks/?long=123.456&lat=78.910&searchRadius=2000&status=REQUESTED&facilityType=Truck

        Response:
        {
            "count": 5,
            "results": [
                {
                    "id": 226,
                    "location": {
                        "latitude": 37.71920021771331,
                        "longitude": -122.39597673109593
                    },
                    "applicant": "Singh Brothers Ice Cream",
                    "facility_type": "Truck",
                    "location_description": "KEY AVE: JENNINGS ST to 03RD ST (1000 - 1068)",
                    "address": "1060 KEY AVE",
                    "status": "REQUESTED",
                    "food_items": [
                        "Ice Cream",
                        " Pre-Packaged Chips",
                        " Candies",
                        " Bottled Water & Canned SODA"
                    ]
                },
                ...
            ]
        }
    """
    def get(self, request):
        longitude = request.query_params.get('long')
        latitude = request.query_params.get('lat')
        search_radius = request.query_params.get('searchRadius', 1000)  # default to 1000 meters if not provided
        truckStatus = request.query_params.get('status')
        facility_type = request.query_params.get('facilityType')

        if not longitude or not latitude:
            return Response(
                {"error": "long and lat are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the coordinates
        longitude, latitude, search_radius, error_message = self.validate_coordinates(longitude, latitude, search_radius)
        if error_message:
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a Point object for the given coordinates
        user_location = Point(longitude, latitude, srid=4326)

        # Filtering by status and facility_type if provided
        filters = Q()
        if truckStatus:
            filters &= Q(status=truckStatus)
        if facility_type:
            filters &= Q(facility_type=facility_type)

        # Filter food trucks by radius using PostGIS
        nearby_food_trucks = FoodTruck.objects.filter(
            filters,
            location__distance_lte=(user_location, search_radius)
        )
        count = nearby_food_trucks.count()

        # If count is less than 5, fetch 5 most closest food trucks since we have to give at least 5 food trucks to choose from
        if count < 5:
            closest_food_trucks = FoodTruck.objects.filter(
                filters
            ).annotate(
                distance=Distance('location', user_location)
            ).order_by('distance')[:5]

            serializer = FoodTruckSerializer(closest_food_trucks, many=True)
            return Response({
                "count": 5,
                "results": serializer.data
            })

        serializer = FoodTruckSerializer(nearby_food_trucks, many=True)

        return Response({
            "count": count,
            "results": serializer.data
        })


    def validate_coordinates(self, longitude, latitude, search_radius):
        """
        Validates the given longitude, latitude, and search radius.

        Args:
            longitude (float): The longitude value to be validated.
            latitude (float): The latitude value to be validated.
            search_radius (float): The search radius value to be validated.

        Returns:
            tuple: A tuple containing the validated longitude, latitude, search radius, and an error message (if any).
                   If the validation is successful, the error message will be None.

        Raises:
            ValueError: If the latitude or longitude is out of range.

        """
        try:
            # Check if latitude and longitude are valid numbers
            longitude = float(longitude)
            latitude = float(latitude)
            search_radius = float(search_radius)
            
            # Check if latitude and longitude are within valid ranges
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude value is out of range (-90 to 90).")
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude value is out of range (-180 to 180).")
            
            return longitude, latitude, search_radius, None  
        except ValueError as e:
            return None, None, None, str(e)
