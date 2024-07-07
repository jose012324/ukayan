from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser,Supply,Cashier,Product

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'quantity', 'price', 'display']

class OutgoingStockForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Supply.objects.all())
    quantity = forms.IntegerField()

class CashierReportForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = ['name', 'date']

class ReportDetailForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(queryset=Supply.objects.all(), to_field_name="name")
    class Meta:
        model = Product
        fields = ['product_name', 'quantity', 'price', 'display', 'expenses','sale']