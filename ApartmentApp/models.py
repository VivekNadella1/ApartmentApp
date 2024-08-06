from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.db.models.signals import post_save

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    phase = models.IntegerField(choices=((1, 'BRP'), (2, 'BPN'), (2, 'BHA')))
    flat_occupancy = models.IntegerField(choices=((1, 'Bachelors'), (2, 'Family')))
    unit_id = models.IntegerField()
    phone_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    emergency_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], blank=True)
    adhar_number = models.IntegerField()
    email = models.EmailField(blank = True)
    rent_and_maintenance = models.FloatField()
    parking = models.FloatField()
    other_payments = models.FloatField(blank=True)
    active = models.BooleanField(default=True)
    furnished = models.BooleanField(default=True)
    internet = models.BooleanField(default=True)
    internet_charge = models.FloatField(blank = True)
    security_deposit = models.IntegerField()
    date_created = models.DateField(default=datetime.date.today)
    start_date = models.DateField(default=datetime.date.today)
    agreement = models.FileField(upload_to='agreements/', null=True, blank=True)
    adhar = models.FileField(upload_to='adhars/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    rent_and_maintance_paid = models.FloatField(blank=True)
    parking_paid = models.FloatField(blank=True)
    internet_paid = models.FloatField(blank=True)
    water_to_be_paid = models.FloatField(blank=True)
    water_paid = models.FloatField(blank=True)
    other_paid = models.FloatField(blank=True)
    transaction_id = models.IntegerField(blank=True)
    payment_type = models.IntegerField(default=1, choices=((1, 'Bank'), (2, 'Cash'), (2, 'Other')))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    transaction_date = models.DateField(default=datetime.date.today)
    date_entered = models.DateField(default=datetime.date.today)
