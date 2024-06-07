from rest_framework import serializers
from .models import FoodTruck

class FoodTruckSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FoodTruck
        fields = '__all__'

    # Override the location field to return latitude and longitude 
    location = serializers.SerializerMethodField()
    def get_location(self, obj):
            return {
                "latitude": obj.location.y,
                "longitude": obj.location.x
            }
