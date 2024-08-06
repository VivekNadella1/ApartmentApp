from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.LoginPage,name='login'),
    path('login/',views.LoginPage,name='login'),
    path('apartments/', views.apartment_list, name='apartment_list'),
    path('logout/',views.LogoutPage,name='logout'),
	path('apartments/add/', views.add_apartment, name='add_apartment'),  
	path('apartments/edit/<int:apartment_id>/', views.edit_apartment, name='edit_apartment'),
    path('apartments/delete/<int:apartment_id>/', views.delete_apartment, name='delete_apartment'),
	path('apartments/<int:apartment_id>/agreement/', views.view_agreement, name='view_agreement'),
    path('apartments/<int:apartment_id>/adhar/', views.view_adhar, name='view_adhar'),
	path('apartments/details/<int:apartment_id>/', views.apartment_details, name='apartment_details'),
    path('apartments/add-payment/<int:apartment_id>/', views.add_payment, name='add_payment'),
	path('payment/edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
	path('apartments/<int:apartment_id>/consolidated-reports/', views.consolidated_reports, name='consolidated_reports'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),    
    path('unpaid-reports/', views.unpaid_reports, name='unpaid_reports'),
	path('export-to-excel/', views.export_to_excel, name='export_to_excel'),
    path('export-confirmation/', views.export_confirmation, name='export_confirmation'),




]