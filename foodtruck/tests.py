from django.urls import reverse
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FoodTruck
from .serializers import FoodTruckSerializer

class FoodTruckListViewTests(APITestCase):
    def setUp(self):
        # Create food truck for testing
        FoodTruck.objects.create(
            location=Point(-122.39597673109593, 37.71920021771331),
            applicant="Singh Brothers Ice Cream",
            facility_type="Truck",
            location_description="KEY AVE: JENNINGS ST to 03RD ST (1000 - 1068)",
            address="1060 KEY AVE",
            status="REQUESTED",
            food_items=[
                "Ice Cream",
                "Pre-Packaged Chips",
                "Candies",
                "Bottled Water & Canned SODA"
            ]
        )

    def test_get_food_trucks_with_valid_coordinates(self):
        url = reverse('foodtrucks')
        data = {
            'long': -122.39597673109593,
            'lat': 37.71920021771331,
            'searchRadius': 2000,
            'status': 'REQUESTED',
            'facilityType': 'Truck'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_food_trucks_with_invalid_coordinates(self):
        url = reverse('foodtrucks')
        data = {
            'long': -200,
            'lat': 100,
            'searchRadius': 2000,
            'status': 'REQUESTED',
            'facilityType': 'Truck'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Latitude value is out of range (-90 to 90).')

    def test_get_food_trucks_without_coordinates(self):
        url = reverse('foodtrucks')
        data = {
            'searchRadius': 2000,
            'status': 'REQUESTED',
            'facilityType': 'Truck'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'long and lat are required fields.')
