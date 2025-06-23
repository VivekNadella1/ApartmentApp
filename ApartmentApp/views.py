import datetime
from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Apartment, Payment
from django.core.paginator import Paginator
from .forms import ApartmentForm, PaymentForm
from django.db.models import Sum, Max
from dateutil.relativedelta import relativedelta
from django.http import FileResponse, QueryDict
from django.http import HttpResponse
import pandas as pd
import io
import datetime

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('apartment_list')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def apartment_list(request):
    show_inactive = request.GET.get('show_inactive') == '1'
    apartments = Apartment.objects.all().order_by('unit_id')
    if not show_inactive:
        apartments = apartments.filter(active=True)
    
    paginator = Paginator(apartments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'show_inactive': show_inactive,
    }

    return render(request, 'apartment_list.html', context)

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

def delete_apartment(request, apartment_id):
    if request.user.is_authenticated and request.user.username == 'SudhirGoli':
        apartment = get_object_or_404(Apartment, id=apartment_id)
        apartment.delete()
        return redirect('apartment_list')
    else:
        return HttpResponse("You are not authorized to delete this apartment.")

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
def apartment_details(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    payment_list = Payment.objects.filter(apartment=apartment)

    paginator = Paginator(payment_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'apartment': apartment,
        'payments': page_obj,
    }

    return render(request, 'apartment_details.html', context)
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

def delete_payment(request, payment_id):
    if request.user.is_authenticated and request.user.username == 'SudhirGoli':
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()
        return redirect('apartment_details', apartment_id=payment.apartment.id)
    else:
        return HttpResponse("You are not authorized to delete this payment.")
    
def consolidated_reports(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    payments = Payment.objects.filter(apartment=apartment)

    consolidated_payments = payments.values('month', 'year').annotate(
        total_rent_and_maintance_paid=Sum('rent_and_maintance_paid'),
        total_water_to_be_paid=Sum('water_to_be_paid'),
        total_water_paid=Sum('water_paid'),
        total_internet_paid=Sum('internet_paid'),
        total_other_paid=Sum('other_paid'),
        total_parking_paid=Sum('parking_paid'),
        latest_transaction_date=Max('transaction_date'),
        latest_date_entered=Max('date_entered')
    )

    paginator = Paginator(consolidated_payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'apartment': apartment,
        'consolidated_payments': page_obj
    }
    return render(request, 'consolidated_reports.html', context)

def monthly_report(request):
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))

        apartments = Apartment.objects.filter(active=True)
        consolidated_report = []

        for apartment in apartments:
            rent_and_maintenance = apartment.rent_and_maintenance
            parking = apartment.parking
            internet_charge = apartment.internet_charge
            other_payments = apartment.other_payments
            payments = Payment.objects.filter(apartment=apartment, month=month, year=year)
            
            print(f"Apartment: {apartment.name}, Payments: {payments}")

            total_rent_and_maintenance_paid = payments.aggregate(Sum('rent_and_maintance_paid'))['rent_and_maintance_paid__sum'] or 0
            total_parking_paid = payments.aggregate(Sum('parking_paid'))['parking_paid__sum'] or 0
            total_internet_paid = payments.aggregate(Sum('internet_paid'))['internet_paid__sum'] or 0
            total_other_paid = payments.aggregate(Sum('other_paid'))['other_paid__sum'] or 0

            unpaid_rent_and_maintenance = rent_and_maintenance - total_rent_and_maintenance_paid
            unpaid_parking = parking - total_parking_paid
            unpaid_internet_charge = internet_charge - total_internet_paid
            unpaid_other_payments = other_payments - total_other_paid
            unpaid = unpaid_rent_and_maintenance + unpaid_internet_charge + unpaid_parking + unpaid_other_payments
            
            consolidated_report.append({
                'apartment': apartment,
                'month': month,
                'year': year,
                'total_rent_and_maintenance_paid': total_rent_and_maintenance_paid,
                'total_parking_paid': total_parking_paid,
                'total_internet_paid': total_internet_paid,
                'total_other_paid': total_other_paid,
                'latest_transaction_date': payments.aggregate(Max('transaction_date'))['transaction_date__max'],
                'latest_date_entered': payments.aggregate(Max('date_entered'))['date_entered__max'],
                'unpaid_rent_and_maintenance': unpaid_rent_and_maintenance,
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
        rent_and_maintenance = apartment.rent_and_maintenance
        parking = apartment.parking
        internet_charge = apartment.internet_charge
        other_payments = apartment.other_payments

        total_rent_and_maintenance_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('rent_and_maintance_paid'))['rent_and_maintance_paid__sum'] or 0
        total_parking_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('parking_paid'))['parking_paid__sum'] or 0
        total_internet_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('internet_paid'))['internet_paid__sum'] or 0
        total_other_paid = Payment.objects.filter(apartment=apartment).aggregate(Sum('other_paid'))['other_paid__sum'] or 0

        current_date = datetime.datetime.now().date()
        months_diff = relativedelta(current_date, apartment.date_created).months

        unpaid_rent_and_maintenance = rent_and_maintenance * months_diff - total_rent_and_maintenance_paid
        unpaid_parking = parking * months_diff - total_parking_paid
        unpaid_internet_charge = internet_charge * months_diff - total_internet_paid
        unpaid_other_payments = other_payments * months_diff - total_other_paid
        total_unpaid = unpaid_rent_and_maintenance + unpaid_other_payments + unpaid_internet_charge + unpaid_parking
        if unpaid_rent_and_maintenance < 0:
            unpaid_rent_and_maintenance = "Extra " + str(abs(unpaid_rent_and_maintenance))
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
            'unpaid_rent_and_maintenance': unpaid_rent_and_maintenance,
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

def export_to_excel(request):
    apartments = Apartment.objects.filter(active=True)
    apartment_data = {
        'Name': [apartment.name for apartment in apartments],
        'Phase': [apartment.phase for apartment in apartments],
        'Unit ID': [apartment.unit_id for apartment in apartments],
        'Phone Number': [apartment.phone_number for apartment in apartments],
        'Emergency Number': [apartment.emergency_number for apartment in apartments],
        'Adhar Number': [apartment.adhar_number for apartment in apartments],
        'Email': [apartment.email for apartment in apartments],
        'Rent and Maintenance': [apartment.rent_and_maintenance for apartment in apartments],
        'Parking': [apartment.parking for apartment in apartments],
        'Other Payments': [apartment.other_payments for apartment in apartments],
        'Active': [apartment.active for apartment in apartments],
        'Furnished': [apartment.furnished for apartment in apartments],
        'Internet': [apartment.internet for apartment in apartments],
        'Internet Charge': [apartment.internet_charge for apartment in apartments],
        'Security Deposit': [apartment.security_deposit for apartment in apartments],
        'Date Created': [apartment.date_created for apartment in apartments],
        'Start Date': [apartment.start_date for apartment in apartments],
        'Agreement': [apartment.agreement.url if apartment.agreement else '' for apartment in apartments],
        'Adhar': [apartment.adhar.url if apartment.adhar else '' for apartment in apartments],
    }
    apartment_df = pd.DataFrame(apartment_data)

    payments = Payment.objects.all()
    payment_data = {
        'Rent and Maintenance Paid': [payment.rent_and_maintance_paid for payment in payments],
        'Parking Paid': [payment.parking_paid for payment in payments],
        'Internet Paid': [payment.internet_paid for payment in payments],
        'Water To Be Paid': [payment.water_to_be_paid for payment in payments],
        'Water Paid': [payment.water_paid for payment in payments],
        'Other Paid': [payment.other_paid for payment in payments],
        'Transaction ID': [payment.transaction_id for payment in payments],
        'Payment Type': [payment.payment_type for payment in payments],
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