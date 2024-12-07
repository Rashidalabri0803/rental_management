from django.contrib import admin
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'unit_type', 'floor_number', 'rent_price', 'status')
    list_filter = ('unit_type', 'status', 'floor_number')
    search_fields = ('unit_number', 'description')
    list_editable = ('status', 'rent_price')
    ordering = ('unit_number',)

    fieldsets = (
        ('المعلومات الأساسية',{
            'fields': ('unit_number', 'unit_type', 'floor_number', 'size', 'description'),
        }),
        ('المعلومات المالية',{
            'fields': ('rent_price', 'status'),
        }),
        ('التواريخ',{
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'national_id')
    search_fields = ('name', 'phone_number', 'national_id', 'email')
    list_filter = ('address',)
    ordering = ('name',)

    fieldsets = (
        ('المعلومات الشخصية',{
            'fields': ('name', 'phone_number', 'email', 'national_id'),
        }),
        ('الموقع',{
            'fields': ('address', 'notes'),
        }),
    )

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    readonly_fields = ('date', 'amount', 'payment_method')
    fields = ('date', 'amount', 'payment_method', 'notes')
    
@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('unit__unit_number', 'tenant__name')
    ordering = ('start_date',)
    inlines = [PaymentInline]

    fieldsets = (
        ('معلومات العقد',{
            'fields': ('unit', 'tenant', 'start_date', 'end_date', 'is_active'),
        }),
        ('المعلومات المالية',{
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
        ('ملاحظات',{
            'fields': ('notes',),
        }),
    )
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'completion_date', 'is_completed')
    list_filter = ('is_completed', 'request_date', 'completion_date')
    search_fields = ('unit__unit_number', 'description')
    ordering = ('-request_date',)
    
    fieldsets = (
        ('معلومات الطلب',{
            'fields': ('unit', 'description', 'request_date'),
        }),
        ('الحالة',{
            'fields': ('completion_date', 'is_completed', 'notes'),
        }),
    )