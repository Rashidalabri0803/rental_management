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

admin.site.register(Tenant)
admin.site.register(Lease)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)
