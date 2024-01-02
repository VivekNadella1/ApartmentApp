from django import forms
from .models import Apartment, Payment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)