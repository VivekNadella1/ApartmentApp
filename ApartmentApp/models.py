from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    phase = models.IntegerField(choices=((1, 'BRP'), (2, 'BPN'), (2, 'BHA')))
    unit_id = models.IntegerField()
    phone_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    emergency_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    adhar_number = models.IntegerField()
    email = models.EmailField()
    rent = models.FloatField()
    maintenance = models.FloatField()
    parking = models.FloatField()
    other_payments = models.FloatField()
    active = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    internet_charge = models.FloatField()
    security_deposit = models.IntegerField()
    date_created = models.DateField(default=datetime.date.today)
    agreement = models.FileField(upload_to='agreements/', null=True, blank=True)
    adhar = models.FileField(upload_to='adhars/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Payment(models.Model):
    rent_paid = models.FloatField()
    maintenance_paid = models.FloatField()
    parking_paid = models.FloatField()
    internet_paid = models.FloatField()
    water_to_be_paid = models.FloatField()
    water_paid = models.FloatField()
    other_paid = models.FloatField()
    transaction_id = models.IntegerField()
    payment_type = models.IntegerField(default=1, choices=((1, 'Bank'), (2, 'Cash'), (2, 'Other')))
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    transaction_date = models.DateField(default=datetime.date.today)
    date_entered = models.DateField(default=datetime.date.today)


def get_month_choices():
    today = datetime.date.today()
    choices = []
    for year in range(today.year - 5, today.year + 1):
        for month in range(1, 13):
            month_name = datetime.date(year, month, 1).strftime('%B')
            choice = (f"{month_name} {year}", f"{month_name} {year}")
            choices.append(choice)
    return choices

class MonthRecord(models.Model):
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    variable = models.IntegerField()

    def __str__(self):
        return f"{self.get_month_display()} {self.year}"

    def get_month_display(self):
        return datetime.date(2000, self.month, 1).strftime('%B')    
    def create_month_records():
        today = datetime.date.today()
        for year in range(today.year - 5, today.year + 1):
            for month in range(1, 13):
                MonthRecord.objects.create(month=month, year=year)
