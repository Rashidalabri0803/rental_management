from django.contrib import admin
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest

admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(Lease)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)
