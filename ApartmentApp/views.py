from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartmentForm, LoginForm, PaymentForm
from .models import Apartment, Payment
from django.forms.models import model_to_dict
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import FileResponse, QueryDict
from django.db.models import F
from django.db.models import Sum, Max
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import pandas as pd
import io
from django.http import StreamingHttpResponse
from datetime import datetime

logged_in = False

logged_in = False

def apartment_list(request):
    show_inactive = request.GET.get('show_inactive') == '1'
    
    sort = request.GET.get('sort')
    sort_asc = request.GET.get('sort_asc') == '1'

    apartments = Apartment.objects.all()

    if not show_inactive:
        apartments = apartments.filter(active=True)

    if sort == 'unit_id':
        apartments = apartments.order_by('unit_id' if sort_asc else '-unit_id')
        sort_asc = not sort_asc
    elif sort == 'rent':
        apartments = apartments.order_by('rent' if sort_asc else '-rent')
        sort_asc = not sort_asc
    elif sort == 'maintenance':
        apartments = apartments.order_by('maintenance' if sort_asc else '-maintenance')
        sort_asc = not sort_asc
    elif sort == 'date_created':
        apartments = apartments.order_by('date_created' if sort_asc else '-date_created')
        sort_asc = not sort_asc
    elif sort == 'other_payments':
        apartments = apartments.order_by('other_payments' if sort_asc else '-other_payments')
        sort_asc = not sort_asc
    elif sort == 'internet_charge':
        apartments = apartments.order_by('internet_charge' if sort_asc else '-internet_charge')
        sort_asc = not sort_asc
    elif sort == 'parking':
        apartments = apartments.order_by('parking' if sort_asc else '-parking')
        sort_asc = not sort_asc
    elif sort == 'security_deposit':
        apartments = apartments.order_by('security_deposit' if sort_asc else '-security_deposit')
        sort_asc = not sort_asc    
    paginator = Paginator(apartments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'show_inactive': show_inactive,
        'sort': sort,
        'sort_asc': sort_asc,
    }

    return render(request, 'apartment_list.html', context)

def delete_apartment(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    apartment.delete()
    return redirect('apartment_list')

def add_apartment(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            apartment = form.save(commit=False)
            agreement = request.FILES.get('agreement')
            if agreement:
                apartment.agreement = agreement
            apartment.save()
            return redirect('apartment_list')
    else:
        form = ApartmentForm()

    return render(request, 'add_apartments.html', {'form': form})

def apartment_details(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    sort = request.GET.get('sort')
    payment_list = Payment.objects.filter(apartment=apartment)

    if sort == 'year':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('year')
        else:
            payment_list = payment_list.order_by('-year')
    elif sort == 'rent_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('rent_paid')
        else:
            payment_list = payment_list.order_by('-rent_paid')
    elif sort == 'maintenance_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('maintenance_paid')
        else:
            payment_list = payment_list.order_by('-maintenance_paid')
    elif sort == 'parking_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('parking_paid')
        else:
            payment_list = payment_list.order_by('-parking_paid')
    elif sort == 'internet_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('internet_paid')
        else:
            payment_list = payment_list.order_by('-internet_paid')
    elif sort == 'water_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('water_paid')
        else:
            payment_list = payment_list.order_by('-water_paid')
    elif sort == 'water_to_be_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('water_to_be_paid')
        else:
            payment_list = payment_list.order_by('-water_to_be_paid')
    elif sort == 'other_paid':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('other_paid')
        else:
            payment_list = payment_list.order_by('-other_paid')
    elif sort == 'transaction_date':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('transaction_date')
        else:
            payment_list = payment_list.order_by('-transaction_date')
    elif sort == 'date_entered':
        if 'sort_asc' in request.GET:
            payment_list = payment_list.order_by('date_entered')
        else:
            payment_list = payment_list.order_by('-date_entered')

    paginator = Paginator(payment_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'apartment': apartment,
        'payments': page_obj,
        'sort': sort
    }

    return render(request, 'apartment_details.html', context)
from .models import Apartment
from .forms import ApartmentForm

def edit_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return redirect('apartment_details', apartment_id=apartment_id)
    else:
        form = ApartmentForm(instance=apartment)

    context = {
        'form': form,
        'apartment': apartment
    }

    return render(request, 'edit_apartment.html', context)

def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    apartment_id = payment.apartment.id

    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment successfully deleted.')
        return HttpResponseRedirect(reverse('apartment_details', kwargs={'apartment_id': apartment_id}))

    return render(request, 'delete_payment.html', {'payment': payment})
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('apartment_details', apartment_id=payment.apartment.id)
    else:
        form = PaymentForm(instance=payment)

    context = {
        'form': form
    }

    return render(request, 'edit_payment.html', context)

from django.shortcuts import render, redirect



from django.core.paginator import Paginator

from django.core.paginator import Paginator

def consolidated_reports(request, apartment_id):
    sort = request.GET.get('sort')
    apartment = Apartment.objects.get(id=apartment_id)
    payments = Payment.objects.filter(apartment=apartment)

    consolidated_payments = payments.values('month', 'year').annotate(
        total_rent_paid=Sum('rent_paid'),
        total_maintenance_paid=Sum('maintenance_paid'),
        total_water_to_be_paid=Sum('water_to_be_paid'),
        total_water_paid=Sum('water_paid'),
        total_internet_paid=Sum('internet_paid'),
        total_other_paid=Sum('other_paid'),
        total_parking_paid=Sum('parking_paid'),
        latest_transaction_date=Max('transaction_date'),
        latest_date_entered=Max('date_entered')
    )

    if sort == 'year':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('year')
        else:
            consolidated_payments = consolidated_payments.order_by('-year')
    elif sort == 'rent_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_rent_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_rent_paid')
    elif sort == 'parking_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_parking_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_parking_paid')
    elif sort == 'internet_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_internet_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_internet_paid')
    elif sort == 'water_to_be_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_water_to_be_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_water_to_be_paid')
    elif sort == 'water_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_water_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_water_paid')
    elif sort == 'other_paid':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('total_other_paid')
        else:
            consolidated_payments = consolidated_payments.order_by('-total_other_paid')
    elif sort == 'transaction_date':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('latest_transaction_date')
        else:
            consolidated_payments = consolidated_payments.order_by('-latest_transaction_date')
    elif sort == 'date_entered':
        if 'sort_asc' in request.GET:
            consolidated_payments = consolidated_payments.order_by('latest_date_entered')
        else:
            consolidated_payments = consolidated_payments.order_by('-latest_date_entered')

    paginator = Paginator(consolidated_payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'apartment': apartment,
        'consolidated_payments': page_obj,
        'sort': sort 
    }

    return render(request, 'consolidated_reports.html', context)
def add_payment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.apartment = apartment
            payment.save()
            return redirect('apartment_details', apartment_id=apartment_id)
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'apartment': apartment
    }

    return render(request, 'add_payment.html', context)

from django.db.models import Sum


def monthly_report(request):
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        sort = request.GET.get('sort')

        apartments = Apartment.objects.filter(active=True)
        consolidated_report = []

        for apartment in apartments:
            rent = apartment.rent
            maintenance = apartment.maintenance
            parking = apartment.parking
            internet_charge = apartment.internet_charge
            other_payments = apartment.other_payments
            payments = Payment.objects.filter(apartment=apartment, month=month, year=year)
            
            print(f"Apartment: {apartment.name}, Payments: {payments}")

            total_rent_paid = payments.aggregate(Sum('rent_paid'))['rent_paid__sum'] or 0
            total_maintenance_paid = payments.aggregate(Sum('maintenance_paid'))['maintenance_paid__sum'] or 0
            total_parking_paid = payments.aggregate(Sum('parking_paid'))['parking_paid__sum'] or 0
            total_internet_paid = payments.aggregate(Sum('internet_paid'))['internet_paid__sum'] or 0
            total_other_paid = payments.aggregate(Sum('other_paid'))['other_paid__sum'] or 0

            print(f"Total Rent Paid: {total_rent_paid}")

            unpaid_rent = rent - total_rent_paid
            unpaid_maintenance = maintenance - total_maintenance_paid
            unpaid_parking = parking - total_parking_paid
            unpaid_internet_charge = internet_charge - total_internet_paid
            unpaid_other_payments = other_payments - total_other_paid
            unpaid = unpaid_rent + unpaid_maintenance + unpaid_internet_charge + unpaid_parking + unpaid_other_payments
            consolidated_report.append({
                'apartment': apartment,
                'month': month,
                'year': year,
                'total_rent_paid': total_rent_paid,
                'total_maintenance_paid': total_maintenance_paid,
                'total_parking_paid': total_parking_paid,
                'total_internet_paid': total_internet_paid,
                'total_other_paid': total_other_paid,
                'latest_transaction_date': payments.aggregate(Max('transaction_date'))['transaction_date__max'],
                'latest_date_entered': payments.aggregate(Max('date_entered'))['date_entered__max'],
                'unpaid_rent': unpaid_rent,
                'unpaid_maintenance': unpaid_maintenance,
                'unpaid_parking': unpaid_parking,
                'unpaid_internet_charge': unpaid_internet_charge,
                'unpaid_other_payments': unpaid_other_payments,
                'unpaid': unpaid,
            })

        print(f"Consolidated Report: {consolidated_report}")

        page_number = request.GET.get('page', 1)
        items_per_page = 10 
        paginator = Paginator(consolidated_report, items_per_page)
        page = paginator.page(page_number)

        context = {
            'consolidated_report': page,
        }
        return render(request, 'monthly_report.html', context)
    else:
        return render(request, 'monthly_report.html')

def unpaid_reports(request):
    apartments = Apartment.objects.filter(active=True)
    unpaid_reports = []

    for apartment in apartments:
        rent = apartment.rent
        maintenance = apartment.maintenance
        parking = apartment.parking
        internet_charge = apartment.internet_charge
        other_payments = apartment.other_payments

        total_rent_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('rent_paid'))['rent_paid__sum'] or 0
        total_maintenance_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('maintenance_paid'))['maintenance_paid__sum'] or 0
        total_parking_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('parking_paid'))['parking_paid__sum'] or 0
        total_internet_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('internet_paid'))['internet_paid__sum'] or 0
        total_other_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('other_paid'))['other_paid__sum'] or 0

        current_date = datetime.datetime.now().date()
        months_diff = relativedelta(current_date, apartment.date_created).months

        unpaid_rent = rent * months_diff - total_rent_paid
        unpaid_maintenance = maintenance * months_diff - total_maintenance_paid
        unpaid_parking = parking * months_diff - total_parking_paid
        unpaid_internet_charge = internet_charge * months_diff - total_internet_paid
        unpaid_other_payments = other_payments * months_diff - total_other_paid
        total_unpaid = unpaid_rent + unpaid_maintenance + unpaid_other_payments + unpaid_internet_charge + unpaid_parking
        if unpaid_rent < 0:
            unpaid_rent = "Extra " + str(abs(unpaid_rent))
        if unpaid_maintenance < 0:
            unpaid_maintenance = "Extra " + str(abs(unpaid_maintenance))
        if unpaid_parking < 0:
            unpaid_parking = "Extra " + str(abs(unpaid_parking))
        if unpaid_internet_charge < 0:
            unpaid_internet_charge = "Extra " + str(abs(unpaid_internet_charge))
        if unpaid_other_payments < 0:
            unpaid_other_payments = "Extra " + str(abs(unpaid_other_payments))
        if total_unpaid < 0:
            total_unpaid = "Extra " + str(abs(total_unpaid))
        unpaid_reports.append({
            'apartment': apartment,
            'unpaid_rent': unpaid_rent,
            'unpaid_maintenance': unpaid_maintenance,
            'unpaid_parking': unpaid_parking,
            'unpaid_internet_charge': unpaid_internet_charge,
            'unpaid_other_payments': unpaid_other_payments,
            'total_unpaid': total_unpaid
        })

    context = {
        'apartments': apartments,
        'unpaid_reports': unpaid_reports,
    }
    return render(request, 'unpaid_reports.html', context)

def view_agreement(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    if apartment.agreement:
        return FileResponse(apartment.agreement)
    else:
        return redirect('apartment_list')
def view_adhar(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    if apartment.adhar:
        return FileResponse(apartment.adhar)
    else:
        return redirect('apartment_details')


from django.http import HttpResponse
import pandas as pd
import io
import datetime

def export_to_excel(request):
    apartments = Apartment.objects.filter(active=True)
    apartment_data = {
        'Name': [apartment.name for apartment in apartments],
        'Phase': [apartment.get_phase_display() for apartment in apartments],
        'Unit ID': [apartment.unit_id for apartment in apartments],
        'Phone Number': [apartment.phone_number for apartment in apartments],
        'Emergency Number': [apartment.emergency_number for apartment in apartments],
        'Adhar Number': [apartment.adhar_number for apartment in apartments],
        'Email': [apartment.email for apartment in apartments],
        'Rent': [apartment.rent for apartment in apartments],
        'Maintenance': [apartment.maintenance for apartment in apartments],
        'Parking': [apartment.parking for apartment in apartments],
        'Other Payments': [apartment.other_payments for apartment in apartments],
        'Active': [apartment.active for apartment in apartments],
        'Furnished': [apartment.furnished for apartment in apartments],
        'Internet': [apartment.internet for apartment in apartments],
        'Internet Charge': [apartment.internet_charge for apartment in apartments],
        'Security Deposit': [apartment.security_deposit for apartment in apartments],
        'Date Created': [apartment.date_created for apartment in apartments],
        'Agreement': [apartment.agreement.url if apartment.agreement else '' for apartment in apartments],
        'Adhar': [apartment.adhar.url if apartment.adhar else '' for apartment in apartments],
    }
    apartment_df = pd.DataFrame(apartment_data)

    payments = Payment.objects.all()
    payment_data = {
        'Rent Paid': [payment.rent_paid for payment in payments],
        'Maintenance Paid': [payment.maintenance_paid for payment in payments],
        'Parking Paid': [payment.parking_paid for payment in payments],
        'Internet Paid': [payment.internet_paid for payment in payments],
        'Water To Be Paid': [payment.water_to_be_paid for payment in payments],
        'Water Paid': [payment.water_paid for payment in payments],
        'Other Paid': [payment.other_paid for payment in payments],
        'Transaction ID': [payment.transaction_id for payment in payments],
        'Payment Type': [payment.get_payment_type_display() for payment in payments],
        'Apartment Name': [payment.apartment.name for payment in payments],
        'Month': [payment.month for payment in payments],
        'Year': [payment.year for payment in payments],
        'Transaction Date': [payment.transaction_date for payment in payments],
        'Date Entered': [payment.date_entered for payment in payments],
    }
    payment_df = pd.DataFrame(payment_data)

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

        apartment_df.to_excel(writer, index=False, sheet_name='Apartments', na_rep='')


        payment_df.to_excel(writer, index=False, sheet_name='Payments', na_rep='')

    excel_buffer.seek(0)


    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="apartments_and_payments.xlsx"'


    response.write(excel_buffer.read())

    return response

def export_confirmation(request):
    return render(request, 'export_confirmation.html')