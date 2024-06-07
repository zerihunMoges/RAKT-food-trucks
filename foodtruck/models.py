from django.db import models

class FoodTruck(models.Model):
    STATUS_CHOICES = (
        ('APPROVED', 'Approved'),
        ('SUSPENDED', 'Suspended'),
        ('REQUESTED', 'Requested'),
        ('EXPIRED', 'Expired'),
    )

    FACILITY_TYPE_CHOICES = (
        ('Truck', 'Truck'),
        ('Push Cart', 'Push Cart'),
        ('Unknown', 'Unknown'),
    )

    applicant = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=255, choices=FACILITY_TYPE_CHOICES)
    location_description = models.TextField()
    address = models.CharField(max_length=255)
  
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    food_items = models.JSONField()
    x =  models.TextField()
    y =  models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
   

    def __str__(self):
        return self.applicant
