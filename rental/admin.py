from django.contrib import admin
from .models import User, Building, Supervisor, SupervisorPermission, Unit, UnitType, Tenant, Lease, Payment, MaintenanceRequest, Invoice, ActivityLog, SupportMessage, Notifiction, MaintenanceReview

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email', 'is_superuser', 'is_tenant', 'is_staff')
    list_filter = ('is_superuser', 'is_tenant', 'is_staff', 'is_active')
    search_fields = ('username', 'phone_number', 'email')
    ordering = ('username',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_units', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SupervisorPermission)
class SupervisorPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'building', 'get_permissions')
    search_fields = ('user__username', 'building__name')
    list_filter = ('building',)

    def get_permissions(self, obj):
        return ', '.join([perm.name for perm in obj.permissions.all()])
    get_permissions.short_description = "الصلاحيات"

@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'building', 'unit_type', 'floor_number', 'rent_price', 'status')
    list_filter = ('building', 'status', 'unit_type')
    search_fields = ('unit_number', 'building__name')
    ordering = ('unit_number',)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant_type', 'national_id', 'company_name', 'address')
    list_filter = ('tenant_type',)
    search_fields = ('user__username', 'national_id', 'company_name')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'start_date', 'end_date')
    search_fields = ('contract_number', 'unit__unit_number', 'tenant__user__username')
    ordering = ('-start_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lease', 'date', 'amount', 'payment_method', 'notes')
    list_filter = ('payment_method', 'date')
    search_fields = ('lease__contract_number',)

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'status', 'notes')
    list_filter = ('status',)
    search_fields = ('unit__unit_number', 'description')
    ordering = ('-request_date',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'lease', 'issue_date', 'due_date', 'total_amount', 'vat', 'paid')
    list_filter = ('paid', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'lease__contract_number')
    ordering = ('-issue_date',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'details')
    search_fields = ('user__username', 'action', 'details')
    ordering = ('-timestamp',)

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at', 'read')
    list_filter = ('read', 'sent_at')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'message')
    ordering = ('-sent_at',)

@admin.register(Notifiction)
class NotifictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)

@admin.register(MaintenanceReview)
class MaintenanceReviewAdmin(admin.ModelAdmin):
    list_display = ('maintenance_request', 'rating', 'feedback')
    search_fields = ('maintenance_request__id', 'feedback')
    ordering = ('maintenance_request__request_date',)