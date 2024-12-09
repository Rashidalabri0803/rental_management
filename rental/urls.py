from django.urls import path
from . import views 
app_name = 'rental'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('supervisor/dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),

    path('buildings/', views.BuildingListView.as_view(), name='building_list'),
    path('buildings/add/', views.BuildingCreateView.as_view(), name='add_building'),
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

    path('leases/', views.LeaseListView.as_view(), name='lease_list'),
    path('leases/add/', views.LeaseCreateView.as_view(), name='add_lease'),
    path('leases/<int:pk>/edit/', views.LeaseUpdateView.as_view(), name='edit_lease'),
    path('leases/<int:pk>/delete/', views.LeaseDeleteView.as_view(), name='delete_lease'),

    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.PaymentCreateView.as_view(), name='add_payment'),

    path('maintenance_requests/', views.MaintenanceRquestListView.as_view(), name='maintenance_request_list'),
    path('maintenance_requests/add/', views.MaintenanceRquestCreateView.as_view(), name='add_maintenance_request'),

    path('invoices/', views.InvoceListView.as_view(), name='invoice_list'),
    path('invoices/add/', views.InvoceCreateView.as_view(), name='add_invoice'),

    path('support_messages/', views.SupportMessageListView.as_view(), name='support_message_list'),
    path('support_messages/add/', views.SupportMessageCreateView.as_view(), name='add_support_message'),

    path('notifictions/', views.NotifictionListView.as_view(), name='notifiction_list'),
]