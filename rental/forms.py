from django import forms
from .models import User, Building, Supervisor, Unit, UnitType, Tenant, Lease, Payment, Notifiction, MaintenanceRequest

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'is_supervisor', 'is_tenant', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'plceholder': 'اسم المستخدم'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'plceholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'plceholder': 'البريد الإلكتروني'}),
            'is_supervisor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_tenant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'total_units']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المبني'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'موقع المبني'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'عدد الوحدات'}),
        }

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['user', 'building']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
        }

class UnitTypeForm(forms.ModelForm):
    class Meta:
        model = UnitType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم النوع'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف النوع'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'building', 'unit_type', 'floor_number', 'size', 'rent_price', 'status']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سعر الإيجار'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['user', 'tenant_type', 'national_id', 'company_name', 'notes']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tenant_type': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم البطاقة المدنية'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الشركة'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية'}),
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'deposit', 'discount', 'status']
        widgets = {
            'contract_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم العقد'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المقدم'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الخصم'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            if start_date and end_date and start_date > end_date:
                raise forms.ValidationError('تاريخ البداية يجب أن يكون قبل تاريخ النهاية.')
            return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['lease', 'date', 'amount', 'payment_method', 'notes']
        widgets = {
            'lease': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية'}),
        }

class NotifictionForm(forms.ModelForm):
    class Meta:
        model = Notifiction
        fields = ['user', 'message', 'type', 'read']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الرسالة'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'status', 'notes']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف الصيانة'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية'}),
        }