from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.db.models.signals import post_save

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    phase = models.IntegerField(choices=((1, 'BRP'), (2, 'BRN'), (3, 'BHIG')))  # Fixed duplicate choice values
    flat_occupancy = models.IntegerField(choices=((1, 'Bachelors'), (2, 'Family'), (3, 'Office'), (4, 'Shop'), (5, 'N/A')))
    unit_id = models.BigIntegerField()  # Changed to BigIntegerField
    phone_number = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)]) 
    emergency_number = models.BigIntegerField(blank=True) 
    adhar_number = models.BigIntegerField()  # Changed to BigIntegerField
    email = models.EmailField(blank=True)
    security_deposit = models.BigIntegerField()  # Changed to BigIntegerField
    rent_and_maintenance = models.BigIntegerField()  # Changed to BigIntegerFiel
    internet_charge = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    parking = models.BigIntegerField()  # Changed to BigIntegerField
    other_payments = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    active = models.BooleanField(default=True)
    furnished = models.BooleanField(default=True)
    internet = models.BooleanField(default=False)
    date_created = models.DateField(default=datetime.date.today)
    start_date = models.DateField(default=datetime.date.today)
    agreement = models.FileField(upload_to='agreements/', null=True, blank=True)
    adhar = models.FileField(upload_to='adhars/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    rent_and_maintance_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    parking_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    internet_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    water_to_be_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    water_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    other_paid = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    transaction_id = models.BigIntegerField(blank=True)  # Changed to BigIntegerField
    payment_type = models.IntegerField(default=1, choices=((1, 'Bank'), (2, 'Cash'), (3, 'Other')))  # Fixed duplicate choice values
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    transaction_date = models.DateField(default=datetime.date.today)
    date_entered = models.DateField(default=datetime.date.today)
