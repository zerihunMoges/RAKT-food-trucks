import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from foodtruck.models import FoodTruck

class Command(BaseCommand):
    help = 'Import food truck data from CSV file'

    def handle(self, *args, **kwargs):
        # Clear the existing data in the FoodTruck model
        FoodTruck.objects.all().delete()
        self.stdout.write(self.style.WARNING('Existing data cleared'))

        with open('foodtruck/management/commands/food-truck-data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_items_list = row['FoodItems'].split(':') if row['FoodItems'] else []
                status = row['Status'].upper() if row['Status'].upper() in dict(FoodTruck.STATUS_CHOICES) else 'UNKNOWN'
                facility_type = row['FacilityType'].title() if row['FacilityType'].title() in dict(FoodTruck.FACILITY_TYPE_CHOICES) else 'Unknown'

                try:
                    latitude = float(row['Latitude'])
                    longitude = float(row['Longitude'])
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid latitude or longitude for {row['Applicant']}"))
                    continue

                location = Point(longitude, latitude, srid=4326)

                FoodTruck.objects.create(
                    applicant=row['Applicant'],
                    facility_type=facility_type,
                    location_description=row['LocationDescription'],
                    address=row['Address'],
                    status=status,
                    food_items=food_items_list,
                    location=location
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
