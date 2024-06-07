from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FoodTruck
from .serializers import FoodTruckSerializer

class FoodTruckListView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        long = request.GET.get('long')

        if lat and long:
            food_trucks = FoodTruck.objects.filter(Q(latitude=lat) & Q(longitude=long))
        else:
            food_trucks = FoodTruck.objects.all()

        serializer = FoodTruckSerializer(food_trucks, many=True)
        return Response(serializer.data)
