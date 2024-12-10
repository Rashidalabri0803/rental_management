from django import forms
from .models import User, Building, Supervisor, SupervisorPermission, Unit, UnitType, Tenant, Lease, Payment, MaintenanceRequest

class UserForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'is_supervisor', 'is_tenant', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
        }

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'total_units']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'إسم المبني'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'موقع المبني', 'rows': 3}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'إجمالي الوحدات'}),
        }

class SupervisorPermissionForm(forms.ModelForm):
    class Meta:
        model = SupervisorPermission
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'اسم الصلاحية'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'وصف الصلاحية', 'rows': 3}),
        }

class UnitTypeForm(forms.ModelForm):
    class Meta:
        model = UnitType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'نوع الوحدة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'وصف النوع', 'rows': 3}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'building', 'unit_type', 'floor_number', 'size', 'rent_price', 'status', 'description']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'رقم الوحدة'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'المساحة'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placehoder': 'سعر الإيجار'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placehoder': 'وصف الوحدة', 'rows': 3}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['user', 'tenant_type', 'national_id', 'company_name', 'address', 'notes']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tenant_type': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'رقم البطاقة المدنية'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placehoder': 'اسم الشركة'}),
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