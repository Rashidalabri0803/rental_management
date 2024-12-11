from django.contrib import admin
from .models import User, Building, Supervisor, Unit, UnitType, Tenant, Lease, Payment, Notifiction, MaintenanceRequest, Invoice, ActivityLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email', 'is_superuser', 'is_tenant', 'is_active')
    list_filter = ('is_superuser', 'is_tenant', 'is_active')
    search_fields = ('username', 'phone_number', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'phone_number', 'email')}),
        ('Permissions', {'fields': ('is_superuser', 'is_tenant', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    fields = ('unit_number', 'unit_type', 'floor_number', 'rent_price', 'status')
    readonly_fields = ('unit_number', 'unit_type', 'status')
    can_delete = False

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'get_rented_units', 'get_available_units', 'created_at')
    search_fields = ('name', 'location', 'address')
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [UnitInline]

    def get_rented_units(self, obj):
        return obj.get_rented_units()
    get_rented_units.short_description = "عدد الوحدات المؤجرة"

    def get_available_units(self, obj):
        return obj.get_available_units()
    get_available_units.short_description = "عدد الوحدات المتاحة"
    
@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'building')
    search_fields = ('user__username', 'building__name')
    list_filter = ('building',)

@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'building', 'unit_type', 'floor_number', 'rent_price', 'status')
    list_filter = ('building', 'status', 'unit_type')
    search_fields = ('unit_number', 'building__name', 'status')
    ordering = ('unit_number',)

class LeaseInline(admin.TabularInline):
    model = Lease
    extra = 0
    fields = ('contract_number', 'unit', 'start_date', 'end_date', 'monthly_rent', 'status')
    readonly_fields = ('contract_number', 'unit', 'status')
    can_delete = False
    
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant_type', 'national_id', 'company_name', 'address')
    list_filter = ('tenant_type',)
    search_fields = ('user__username', 'national_id', 'company_name')
    ordering = ('user__username',)
    inlines = [LeaseInline]

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'start_date', 'end_date')
    search_fields = ('contract_number', 'unit__unit_number', 'tenant__user__username')
    ordering = ('-start_date',)
    actions = ['mark_expired', 'terminate_lease']

    def mark_expired(self, request, queryset):
        expired_leases = queryset.filter(end_date__lt=date.today())
        expired_leases.update(status='Expired', is_active=False)
        self.message_user(request, f"{expired_leases.count()} عقد تم تحديده كمنتهي.")
    mark_expired.short_description = "تحديد العقود المنتهية"

    def terminate_lease(self, request, queryset):
        queryset.update(is_active=False, status='suspended')
        self.message_user(request, f"{queryset.count()} عقد تم إيقافه.")
    terminate_lease.short_description = "إيقاف العقود المحددة"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lease', 'date', 'amount', 'payment_method', 'notes')
    list_filter = ('payment_method', 'date')
    search_fields = ('lease__contract_number', 'amount')
    ordering = ('-date',)

@admin.register(Notifiction)
class NotifictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'type', 'created_at', 'read')
    list_filter = ('type', 'read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'delete_notifiction']

    def mark_as_read(self, request, queryset):
        updated_count = queryset.updaye(read=True)
        self.message_user(request, f"{updated_count} إشعار تم تحديده كمقروءة.")
    mark_as_read.short_description = "تحديد الإشعارات كمقروءة"

    def delete_notifiction(self, request, queryset):
        deleted_count = queryset.delete()[0]
        self.message_user(request, f"{deleted_count} إشعار تم حذفه.")
    delete_notifiction.short_description = "حذف الإشعارات المحددة"

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description', 'request_date', 'status', 'notes')
    list_filter = ('status', 'request_date')
    search_fields = ('unit__unit_number', 'description', 'notes')
    ordering = ('-request_date',)
    actions = ['mark_completed', 'mark_as_in_progress']

    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status='completed')
        self.message_user(request, f"{updated_count} طلب تم تحديده كمكتمل.")
    mark_as_completed.short_description = "تحديد الطلبات المكتملة"

    def mark_as_in_progress(self, request, queryset):
        updated_count = queryset.update(status='in progress')
        self.message_user(request, f"{updated_count} طلب تم تحديده كتحت للتنفيذ.")
    mark_as_in_progress.short_description = "تحديد الطلبات كتحت التنفيذ"

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'lease', 'issue_date', 'due_date', 'total_amount', 'status')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'lease__contract_number', 'total_amount')
    ordering = ('-issue_date',)
    actions = ['mark_as_paid', 'mark_as_unpaid']

    def mark_as_paid(self, request, queryset):
        updated_count = queryset.update(status='paid')
        self.message_user(request, f"{updated_count} فاتورة تم تحديده كمدفوعة.")
    mark_as_paid.short_description = "تحديد الفواتير المدفوعة"

    def mark_as_unpaid(self, request, queryset):
        updated_count = queryset.update(status='unpaid')
        self.message_user(request, f"{updated_count} فاتورة تم تحديده كغير مدفوعة.")
    mark_as_unpaid.short_description = "تحديد الفواتير غير مدفوعة"

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'details')
    list_filter = ('timestamp')
    search_fields = ('user__username', 'action', 'details')
    ordering = ('-timestamp',)