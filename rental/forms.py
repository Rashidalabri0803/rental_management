from django import forms
from .models import Lease, UnitType, MaintenanceRequest, Payment, Invoice, ActivityLog, SupportMessage, Notifiction, MaintenanceReview, SupervisorPermission, Unit, Supervisor, Tenant, Building, UnitType, SupervisorPermission, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'is_supervisor', 'is_tenant', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الهاتف'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}),
            'is_supervisor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_tenant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'total_units']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المبني'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'موقع المبني'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'إجمالي الوحدات'}),
        }

class SupervisorPermissonForm(forms.ModelForm):
    class Meta:
        model = SupervisorPermission
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الصلاحية'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف الصلاحية'}),
        }

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['user', 'building', 'permissions']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class UnitTypeForm(forms.ModelForm):
    class Meta:
        model = UnitType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم نوع الوحدة'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف النوع'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'building', 'unit_type', 'floor_number', 'size', 'rent_price', 'status', 'description']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الوحدة'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'unit_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'رقم الطابق'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المساحة'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سعر الإيجار'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف الوحدة'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['user', 'tenant_type', 'national_id', 'company_name', 'address', 'notes']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tenant_type': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم البطاقة المدنية'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الشركة'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'عنوان المستأجر'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات إضافية'}),
        }

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'deposit', 'status', 'is_active']
        widgets = {
            'contract_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم العقد'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الإيجار الشهري'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المقدم'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

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

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['lease', 'invoice_number', 'issue_date', 'due_date', 'total_amount', 'vat', 'paid']
        widgets = {
            'lease': forms.Select(attrs={'class': 'form-control'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الفاتورة'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'إجمالي المبلغ'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ضريبة القيمة المضافة (%)'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SuppMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['sender', 'recipient', 'subject', 'message']
        widgets = {
            'sender': forms.Select(attrs={'class': 'form-control'}),
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الرسالة'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'الرسالة'}),
        }

class NotifictionForm(forms.ModelForm):
    class Meta:
        model = Notifiction
        fields = ['user', 'message', 'read']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الرسالة'}),
            'read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MaintenanceReviewForm(forms.ModelForm):
    class Meta:
        model = MaintenanceReview
        fields = ['maintenance_request', 'rating', 'feedback']
        widgets = {
            'maintenance_request': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'التقييم (1-5)'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ملاحظات'}),
        }