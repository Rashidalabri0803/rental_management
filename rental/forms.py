from django import forms
from .models import User, Building, Supervisor, Unit, Tenant, Lease, Payment, MaintenanceRequest

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
        label='رقم الهاتف', 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
        label='كلمة المرور', 
    )

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'total_units']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'إسم المبني'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'موقع المبني', 'rows': 3}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'إجمالي الوحدات'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['user', 'tenant_type', 'national_id', 'address', 'notes']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tenant_type': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'رقم البطاقة المدنية'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'عنوان المستأجر'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'ملاحظات إضافية', 'rows': 3}),
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'deposit', 'is_active']
        widgets = {
            'contract_number': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'رقم العقد'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'الإيجار الشهري'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'المقدم'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }