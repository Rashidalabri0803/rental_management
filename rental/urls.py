from django.urls import path
from . import views 
app_name = 'rental'
urlpatterns = [
    path('builings/', views.BuildingListView.as_view(), name='building_list'),
    path('buildings/add/', views.BuildingCrateView.as_view(), name='add_building'),
    path('buildings/<int:pk>/edit/', views.BuildingUpdateView.as_view(), name='edit_building'),
    path('buildings/<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='delete_building'),

    path('units/', views.UnitListView.as_view(), name='unit_list'),
    path('units/add/', views.UnitCreateView.as_view(), name='add_unit'),
    path('units/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='edit_unit'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='delete_unit'),

    path('tenants/', views.TenantListView.as_view(), name='tenant_list'),
    path('tenants/add/', views.TenantCreateView.as_view(), name='add_tenant'),
    path('tenants/<int:pk>/edit/', views.TenantUpdateView.as_view(), name='edit_tenant'),
    path('tenants/<int:pk>/delete/', views.TenantDeleteView.as_view(), name='delete_tenant'),

    path('supervisors/', views.SupervisorListView.as_view(), name='supervisor_list'),
    path('supervisors/add/', views.SupervisorCreateView.as_view(), name='add_supervisor'),
    path('supervisors/<int:pk>/edit/', views.SupervisorUpdateView.as_view(), name='edit_supervisor'),
    path('supervisors/<int:pk>/delete/', views.SupervisorDeleteView.as_view(), name='delete_supervisor'),

    path('leases/', views.LeaseListView.as_view(), name='lease_list'),
    path('leases/add/', views.LeaseCreateView.as_view(), name='add_lease'),

    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.PaymentCreateView.as_view(), name='add_payment'),

    path('maintenance/', views.MaintenanceRequestListView.as_view(), name='maintenance_request_list'),
    path('maintenance/add/', views.MaintenanceRequestCreateView.as_view(), name='add_maintenance_request'),
    path('maintenance/<int:pk>/edit/', views.MaintenanceRequestUpdateView.as_view(), name='edit_maintenance_request'),
]