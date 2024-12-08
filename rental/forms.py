from django import forms
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest
from django.core.exceptions import ValidationError

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'unit_type', 'floor_number', 'size', 'rent_price', 'electricity_meter_number', 'water_meter_number', 'status', 'description']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة بالمتر المربع'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سعر الإيجار الشهري'}),
            'electricity_meter_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم عداد الكهرباء'}),
            'water_meter_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم عداد المياه'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف الوحدة', 'rows': 3}),
        }
        labels = {
            'unit_number': 'رقم الوحدة',
            'unit_type': 'نوع الوحدة',
            'floor_number': 'رقم الطابق',
            'size': 'المساحة بالمتر المربع',
            'rent_price': 'سعر الإيجار الشهري',
            'electricity_meter_number': 'رقم عداد الكهرباء',
            'water_meter_number': 'رقم عداد المياه',
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
            #'commercial_record': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم السجل التجاري (للمستأجرين التجاريين)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ملاحظات إضافية', 'rows': 3}),
        }
        labels = {
            'name': 'اسم المستأجر',
            'phone_number': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'national_id': 'رقم الهوية الوطنية',
            'address': 'عنوان الإقامة',
            'commercial_record': 'رقم السجل التجاري',
            'notes': 'ملاحظات إضافية',
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'duration_months', 'monthly_rent', 'deposit', 'contract_file', 'is_active']
        widgets = {
            'contract_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم العقد'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مدة العقد (بالشهور)'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المقدم'}),
            'contract_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'contract_number': 'رقم العقد',
            'unit': 'الوحدة',
            'tenant': 'المستأجر',
            'start_date': 'تاريخ بداية العقد',
            'end_date': 'تاريخ نهاية العقد',
            'duration_months': 'مدة العقد (بالأشهر)',
            'monthly_rent': 'الإيجار الشهري (ريال عماني)',
            'deposit': 'المقدم (ريال عماني)',
            'contract_file': 'ملف العقد',
            'is_active': 'العقد نشط',
        }

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            duration_months = cleaned_data.get('duration_months')
            if start_date and end_date and start_date >= end_date:
                raise forms.ValidationError("تاريخ نهاية العقد يجب أن يكون بعد تاريخ البداية.")
            if start_date and end_date and duration_months:
                calculated_duration = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                if calculated_duration != duration_months:
                    raise forms.ValidationError("مدة العقد لا تتطابق مع التواريخ المدخلة")
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
            'amount': 'المبلغ المدفوع (ريال عماني)',
            'payment_method': 'طريقة الدفع',
            'notes': 'ملاحظات إضافية',
        }

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'status', 'start_date', 'completion_date', 'notes']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'وصف المشكلة', 'rows': 3}),
            #'request_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'ملاحظات إضافية', 'rows': 3}),
        }
        labels = {
            'unit': 'الوحدة',
            'description': 'وصف المشكلة',
            #'request_date': 'تاريخ الطلب',
            'status': 'حالة الطلب',
            'start_date': 'تاريخ بدء الصيانة',
            'completion_date': 'تاريخ إنهاء الصيانة',
            'notes': 'ملاحظات إضافية',
        }