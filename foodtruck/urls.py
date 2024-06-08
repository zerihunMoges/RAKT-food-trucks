from django.urls import path
from .views import FoodTruckListView

urlpatterns = [
    path('foodtrucks/', FoodTruckListView.as_view(), name='foodtrucks'),
]
