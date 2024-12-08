from django.contrib import admin
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'unit_type', 'floor_number', 'rent_price', 'status')
    list_filter = ('unit_type', 'status', 'floor_number')
    search_fields = ('unit_number', 'description')
    ordering = ('unit_number',)
    list_editable = ('status', 'rent_price')

    fieldsets = (
        ('المعلومات الأساسية',{
            'fields': ('unit_number', 'unit_type', 'floor_number', 'size', 'description'),
        }),
        ('التفاصيل المالية',{
            'fields': ('rent_price', 'status', 'electricity_meter_number', 'water_meter_number'),
        }),
        ('التواريخ',{
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'national_id', 'commercial_record')
    search_fields = ('name', 'phone_number', 'national_id', 'commercial_record')
    list_filter = ('commercial_record',)
    ordering = ('name',)

    fieldsets = (
        ('المعلومات الشخصية',{
            'fields': ('name', 'phone_number', 'email', 'national_id'),
        }),
        ('السجل التجاري والموقع',{
            'fields': ('commercial_record', 'address', 'notes'),
        }),
    )

class PaymentInline(admin.TabularInline):
    """عرض المدفوعات المرتبطة بعقد إيجار داخل لوحة الإدارة."""
    model = Payment
    extra = 0
    readonly_fields = ('date', 'amount', 'payment_method')
    fields = ('date', 'amount', 'payment_method', 'notes')
    
@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('contract_number', 'unit__unit_number', 'tenant__name')
    ordering = ('start_date',)
    inlines = [PaymentInline]

    fieldsets = (
        ('معلومات العقد',{
            'fields': ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'duration_months', 'is_active'),
        }),
        ('التفاصيل المالية',{
            'fields': ('monthly_rent', 'deposit', 'contract_file'),
        }),
    )
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lease', 'date', 'amount', 'payment_method')
    list_filter = ('payment_method', 'date')
    search_fields = ('lease__unit__unit_number', 'amount')
    ordering = ('-date',)

    fieldsets = (
        ('معلومات الدفع',{
            'fields': ('lease', 'date', 'amount', 'payment_method'),
        }),
        ('ملاحظات إضافية',{
            'fields': ('notes',),
        }),
    )
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'status',  'completion_date')
    list_filter = ('status', 'request_date', 'completion_date')
    search_fields = ('unit__unit_number', 'description')
    ordering = ('-request_date',)
    
    fieldsets = (
        ('تفاصيل الطلب',{
            'fields': ('unit', 'description', 'request_date', 'status'),
        }),
        ('التواريخ والملاحظات',{
            'fields': ('start_date', 'completion_date', 'notes'),
        }),
    )