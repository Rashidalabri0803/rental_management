from django.urls import path
from . import views

urlpatterns = [
    path('units/', views.unit_list, name='unit_list'),
    path('units/add/', views.add_unit, name='add_unit'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('units/<int:pk>/edit/', views.edit_unit, name='edit_unit'),
    path('units/<int:pk>/delete/', views.delete_unit, name='delete_unit'),

    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),
    path('tenants/<int:pk>/edit/', views.edit_tenant, name='edit_tenant'),
    path('tenants/<int:pk>/delete/', views.delete_tenant, name='delete_tenant'),

    path('leases/', views.lease_list, name='lease_list'),
    path('leases/add/', views.add_lease, name='add_lease'),
    path('leases/<int:pk>/edit/', views.edit_lease, name='edit_lease'),
    path('leases/<int:pk>/delete/', views.delete_lease, name='delete_lease'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.add_payment, name='add_payment'),

    path('maintenancers/', views.maintenance_request_list, name='maintenancer_list'),
    path('maintenancers/add/', views.add_maintenance_request, name='add_maintenance_request'),
    path('maintenancers/<int:pk>/edit/', views.edit_maintenance_request, name='edit_maintenance_request'),
]