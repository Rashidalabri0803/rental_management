from django import forms
from django.core.exceptions import ValidationError
from .models import User, Building, Unit, Tenant, Lease, Payment, Notifiction, MaintenanceRequest, Invoice
from datetime import date

class TenantRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور'}),
        label="تأكيد كلمة المرور"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة المرور'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('كلمة المرور غير متطابقة')

        return cleaned_data

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'total_units', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المبني'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'موقع المبني'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'نوع الوحدة'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'إجمالي الوحدات'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان المبني'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'building', 'unit_type', 'floor_number', 'size', 'rent_price', 'status', 'description']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'نوع الوحدة'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة (متر مربع)'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سعر الإيجار'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف الوحدة'}),
        }

    def clean_rent_price(self):
        rent_price = self.cleaned_data.get('rent_price')
        if rent_price <= 0:
            raise ValidationError("سعر الإيجار يجب أن يكون أكبر من صفر")
        return rent_price
        
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
                raise forms.ValidationError("تاريخ البداية يجب أن يكون قبل تاريخ النهاية.")
            return cleaned_data

        def clean_monthly_rent(self):
            monthly_rent = self.cleaned_data.get('monthly_rent')
            if monthly_rent <= 0:
                raise forms.ValidationError("الإيجار الشهري يجب أن يكون أكبر من صفر")
            return monthly_rent

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['lease', 'amount', 'payment_method', 'notes']
        widgets = {
            'lease': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ المدفوع'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية'}),
        }

class MainenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['unit', 'description', 'status', 'notes']
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف الطلب'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات'}),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("وصف الطلب يجب أن يكون أقل من 10 حرف.")
        return description
        
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'lease', 'due_date', 'total_amount', 'status']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الفاتورة'}),
            'lease': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ الإجمالي'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < date.today():
            raise forms.ValidationError("تاريخ الاستحقاق يجب أن يكون في المستقبل")
        return due_date