from django import forms
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'unit_type', 'floor_number', 'size', 'rent_price' , 'status', 'description']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة بالمتر المربع'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سعر الإيجار الشهري'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف الوحدة', 'rows': 3}),
        }
        labels = {
            'unit_number': 'رقم الوحدة',
            'unit_type': 'نوع الوحدة',
            'floor_number': 'رقم الطابق',
            'size': 'المساحة بالمتر المربع',
            'rent_price': 'سعر الإيجار الشهري',
            'status': 'حالة الوحدة',
            'description': 'وصف الوحدة',
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone_number', 'email', 'national_id', 'address', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستأجر'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهوية الوطنية'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الإقامة'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ملاحظات إضافية', 'rows': 3}),
        }
        labels = {
            'name': 'اسم المستأجر',
            'phone_number': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'national_id': 'رقم الهوية الوطنية',
            'address': 'عنوان الإقامة',
            'notes': 'ملاحظات إضافية',
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'deposit', 'contract_file', 'is_active']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المقدم'}),
            'contract_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'unit': 'الوحدة',
            'tenant': 'المستأجر',
            'start_date': 'تاريخ بداية العقد',
            'end_date': 'تاريخ نهاية العقد',
            'monthly_rent': 'الإيجار الشهري',
            'deposit': 'المقدم',
            'contract_file': 'ملف العقد',
            'is_active': 'العقد نشط',
        }

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            if start_date and end_date and start_date >= end_date:
                raise forms.ValidationError('تاريخ نهاية العقد يجب أن يكون بعد تاريخ البداية.')
            return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['lease', 'date', 'amount', 'payment_method', 'notes']
        widgets = {
            'lease': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ المدفوع'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ملاحظات إضافية', 'rows': 3}),
        }
        labels = {
            'lease': 'عقد الإيجار',
            'date': 'تاريخ الدفع',
            'amount': 'المبلغ المدفوع',
            'payment_method': 'طريقة الدفع',
            'notes': 'ملاحظات إضافية',
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'completion_date', 'is_completed', 'notes']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف المشكلة', 'rows': 3}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ملاحظات إضافية', 'rows': 3}),
        }
        labels = {
            'unit': 'الوحدة',
            'description': 'وصف المشكلة',
            'completion_date': 'تاريخ الإنجاز',
            'is_completed': 'تم الإنجاز',
            'notes': 'ملاحظات إضافية',
        }