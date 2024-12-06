from django.urls import path
from . import views

urlpatterns = [
    path('units/', views.unit_list, name='unit_list'),
    path('units/add/', views.unit_create, name='add_unit'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('units/<int:pk>/edit/', views.unit_update, name='edit_unit'),
    path('units/<int:pk>/delete/', views.unit_delete, name='delete_unit'),

    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.tenant_create, name='add_tenant'),
    path('tenants/<int:pk>/edit/', views.tenant_update, name='edit_tenant'),
    path('tenants/<int:pk>/delete/', views.tenant_delete, name='delete_tenant'),

    path('leases/', views.lease_list, name='lease_list'),
    path('leases/add/', views.lease_create, name='add_lease'),
    path('leases/<int:pk>/edit/', views.lease_update, name='edit_lease'),
    path('leases/<int:pk>/delete/', views.lease_delete, name='delete_lease'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_create, name='add_payment'),

    path('maintenancers/', views.maintenance_request_list, name='maintenancer_list'),
    path('maintenancers/add/', views.maintenance_request_create, name='add_maintenance_request'),
    path('maintenancers/<int:pk>/edit/', views.maintenance_request_update, name='edit_maintenance_request'),
]