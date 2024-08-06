from django.contrib import admin
from .models import Apartment, Payment

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'flat_occupancy', 'unit_id', 'phone_number', 'email', 'rent_and_maintenance', 'parking', 'active', 'furnished', 'internet', 'date_created', 'start_date')
    search_fields = ('name', 'unit_id', 'phone_number', 'email')
    list_filter = ('phase', 'flat_occupancy', 'active', 'furnished', 'internet')
    fieldsets = (
        (None, {
            'fields': ('name', 'phase', 'flat_occupancy', 'unit_id', 'phone_number', 'emergency_number', 'adhar_number', 'email', 'rent_and_maintenance', 'parking', 'other_payments', 'active', 'furnished', 'internet', 'internet_charge', 'security_deposit', 'date_created', 'start_date', 'agreement', 'adhar')
        }),
    )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'month', 'year', 'transaction_id', 'payment_type', 'transaction_date', 'date_entered')
    search_fields = ('apartment__name', 'transaction_id')
    list_filter = ('payment_type', 'month', 'year')
    fieldsets = (
        (None, {
            'fields': ('apartment', 'rent_and_maintance_paid', 'parking_paid', 'internet_paid', 'water_to_be_paid', 'water_paid', 'other_paid', 'transaction_id', 'payment_type', 'month', 'year', 'transaction_date', 'date_entered')
        }),
    )

admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Payment, PaymentAdmin)
