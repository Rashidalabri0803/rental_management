from django.contrib import admin
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest

admin.site.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'unit_type', 'floor_number', 'rent_price', 'status', 'is_available')
    list_filter = ('unit_type', 'status', 'floor_number')
    search_fields = ('unit_number', 'desription')
    list_editable = ('status', 'rent_price')
    ordering = ('unit_number',)

    fieldsets = (
        ('المعلومات الأساسية',{
            'fields': ('unit_number', 'unit_type', 'floor_number', 'size', 'desription'),
        }),
        ('المعلومات المالية',{
            'fields': ('rent_price', 'status', 'is_available'),
        }),
        ('التواريخ',{
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Unit, UnitAdmin)
admin.site.register(Tenant)
admin.site.register(Lease)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)
