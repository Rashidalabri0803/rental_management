from django.urls import path
from . import views 
app_name = 'rental'
urlpatterns = [
    path('buildings/', BuildingListView.as_view(), name='building_list'),
    path('buildings/add/', BuildingCreateView.as_view(), name='add_building'),
    path('buildings/<int:pk>/edit/', BuildingUpdateView.as_view(), name='edit_building'),
    path('buildings/<int:pk>/delete/', BuildingDeleteView.as_view(), name='delete_building'),

    path('supervisors/', SupervisorListView.as_view(), name='supervisor_list'),
    path('supervisors/add/', SupervisorCreateView.as_view(), name='add_supervisor'),
    path('supervisors/<int:pk>/edit/', SupervisorUpdateView.as_view(), name='edit_supervisor'),
    path('supervisors/<int:pk>/delete/', SupervisorDeleteView.as_view(), name='delete_supervisor'),

    path('units/', UnitListView.as_view(), name='unit_list'),
    path('units/add/', UnitCreateView.as_view(), name='add_unit'),
    path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='edit_unit'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='delete_unit'),

    path('tenants/', LeaseListView.as_view(), name='tenant_list'),
    path('tenants/add/', LeaseCreateView.as_view(), name='add_tenant'),
    path('tenants/<int:pk>/edit/', LeaseUpdateView.as_view(), name='edit_tenant'),
    path('tenants/<int:pk>/delete/', LeaseDeleteView.as_view(), name='delete_tenant'),

    path('leases/', LeaseListView.as_view(), name='lease_list'),
    path('leases/add/', LeaseCreateView.as_view(), name='add_lease'),
    path('leases/<int:pk>/edit/', LeaseUpdateView.as_view(), name='edit_lease'),
    path('leases/<int:pk>/delete/', LeaseDeleteView.as_view(), name='delete_lease'),

    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', PaymentCreateView.as_view(), name='add_payment'),

    path('maintenance/', MaintenanceRequestListView.as_view(), name='maintenance_request_list'),
    path('maintenance/add/', MaintenanceRequestCreateView.as_view(), name='add_maintenance_request'),
    path('maintenance/<int:pk>/edit/', MaintenanceRequestUpdateView.as_view(), name='edit_maintenance_request'),
    path('maintenance/<int:pk>/delete/', MaintenanceRequestDeleteView.as_view(), name='delete_maintenance_request')و
]