from django.contrib import admin
from .models import User, Building, Supervisor, Unit, Tenant, Lease, Payment, MaintenanceRequest

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_superuser', 'is_tenant')
    list_filter = ('is_superuser', 'is_tenant')
    search_fields = ('username', 'phone_number')
    ordering = ('username',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """إدارة المباني"""
    list_display = ('name', 'location', 'total_units', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    readonly_fields = ('status',)

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    """إدارة المشرفين"""
    list_display = ('user', 'building', 'permissions')
    search_fields = ('user__username', 'building__name')
    list_filter = ('building',)
    
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'building', 'unit_type', 'floor_number', 'rent_price', 'status')
    list_filter = ('building', 'status')
    search_fields = ('unit_number', 'building__name')
    ordering = ('unit_number',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant_type', 'national_id',  'address')
    search_fields = ('user__username', 'national_id')
    list_filter = ('tenant_type',)

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    """إدارة عقود الإيجار"""
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('contract_number', 'unit__unit_number', 'tenant__user__username')
    ordering = ('-start_date',)
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """إدارة المدفوعات"""
    list_display = ('lease', 'date', 'amount', 'payment_method')
    list_filter = ('payment_method', 'date')
    search_fields = ('lease__contract_number',)
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    """إدارة طلبات الصيانة"""
    list_display = ('unit', 'description', 'requested_by', 'status')
    list_filter = ('status',)
    search_fields = ('unit__unit_number', 'description')