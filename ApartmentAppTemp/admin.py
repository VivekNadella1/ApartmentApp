from django.contrib import admin
from .models import Apartment, Payment, MonthRecord
from django.contrib import admin
from .models import MonthRecord
class MonthRecordAdmin(admin.ModelAdmin):
    list_display = ('get_month_display', 'year', 'variable')
    list_filter = ('year',)
    search_fields = ('year',)

    def get_month_display(self, obj):
        return obj.get_month_display()

    get_month_display.short_description = 'Month'
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'unit_id', 'phone_number', 'emergency_number', 'adhar_number', 'email', 'rent', 'maintenance', 'parking', 'other_payments', 'active', 'furnished', 'internet', 'internet_charge', 'date_created')
    search_fields = ('name', 'email')
    fields = ('name', 'phase', 'unit_id', 'email')
    inlines = [PaymentInline]


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Payment)
admin.site.register(MonthRecord, MonthRecordAdmin)
