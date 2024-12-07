from django.urls import path
from .views import UnitListView, UnitCreateView, UnitUpdateView, UnitDeleteView, UnitDetailView, LeaseListView, LeaseCreateView, LeaseUpdateView, LeaseDeleteView, PaymentListView, PaymentCreateView, MaintenanceRequestListView, MaintenanceRequestCreateView, MaintenanceRequestUpdateView

urlpatterns = [
    path('units/', UnitListView.as_view(), name='unit_list'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
    path('units/add/', UnitCreateView.as_view(), name='add_unit'),
    path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='edit_unit'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='delete_unit'),

    path('tenants/', LeaseListView.as_view(), name='lease_list'),
    path('tenants/add/', LeaseCreateView.as_view(), name='add_lease'),
    path('tenants/<int:pk>/edit/', LeaseUpdateView.as_view(), name='edit_lease'),
    path('tenants/<int:pk>/delete/', LeaseDeleteView.as_view(), name='delete_lease'),

    path('leases/', LeaseListView.as_view(), name='lease_list'),
    path('leases/add/', LeaseCreateView.as_view(), name='add_lease'),
    path('leases/<int:pk>/edit/', LeaseUpdateView.as_view(), name='edit_lease'),
    path('leases/<int:pk>/delete/', LeaseDeleteView.as_view(), name='delete_lease'),

    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', PaymentCreateView.as_view(), name='add_payment'),

    path('maintenance_requests/', MaintenanceRequestListView.as_view(), name='maintenance_request_list'),
    path('maintenance_requests/add/', MaintenanceRequestCreateView.as_view(), name='add_maintenance_request'),
    path('maintenance_requests/<int:pk>/edit/', MaintenanceRequestUpdateView.as_view(), name='edit_maintenance_request'),
]