from django.contrib import admin
from .models import Building, Unit, Tenant, Supervisor, Lease, Payment, MaintenanceRequest

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """إدارة المباني"""
    list_display = ('name', 'location', 'total_units', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('تفاصيل المبني',{
            'fields': ('name', 'location', 'facilities'),
        }),
        ('التواريخ',{
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def total_units(self, obj):
        return obj.unit_set.count()
    total_units.short_description = "إجمالي الوحدات"

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'building', 'unit_type', 'floor_number', 'rent_price', 'status', 'is_available')
    list_filter = ('building', 'unit_type', 'status', 'floor_number')
    search_fields = ('unit_number', 'building__name', 'description')
    ordering = ('unit_number',)
    list_editable = ('status', 'rent_price')

    fieldsets = (
        ('تفاصيل الوحدة',{
            'fields': ('building', 'unit_number', 'unit_type', 'floor_number', 'size', 'description'),
        }),
        ('المعلومات المالية',{
            'fields': ('rent_price', 'status', 'electricity_meter_number', 'water_meter_number'),
        }),
    )

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'national_id', 'email', 'address')
    search_fields = ('name', 'phone_number', 'national_id')
    list_filter = ('address',)
    ordering = ('name',)

    fieldsets = (
        ('معلومات المستأجر',{
            'fields': ('name', 'phone_number', 'email', 'national_id', 'address'),
        }),
        ('ملاحظات إضافية',{
            'fields': ('notes',),
        }),
    )

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    """إدارة المشرفين"""
    list_display = ('user', 'building', 'phone_number')
    search_fields = ('user__username', 'building__name', 'phone_number')
    list_filter = ('building',)
    ordering = ('user__username',)
    fieldsets = (
        ('تفاصيل المشرف',{
            'fields': ('user', 'building', 'phone_number'),
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
    """إدارة عقود الإيجار"""
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('contract_number', 'unit__unit_number', 'tenant__name')
    ordering = ('start_date',)
    inlines = [PaymentInline]

    fieldsets = (
        ('تفاصيل العقد',{
            'fields': ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'duration_months', 'is_active'),
        }),
        ('التفاصيل المالية',{
            'fields': ('monthly_rent', 'deposit', 'contract_file'),
        }),
    )
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """إدارة المدفوعات"""
    list_display = ('lease', 'date', 'amount', 'payment_method')
    list_filter = ('payment_method', 'date')
    search_fields = ('lease__unit__unit_number', 'amount')
    ordering = ('-date',)

    fieldsets = (
        ('تفاصيل الدفع',{
            'fields': ('lease', 'date', 'amount', 'payment_method'),
        }),
        ('ملاحظات إضافية',{
            'fields': ('notes',),
        }),
    )
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    """إدارة طلبات الصيانة"""
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