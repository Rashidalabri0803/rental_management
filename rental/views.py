from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Building,Unit,Tenant,Lease,Payment,MaintenanceRequest,Invoice,SupportMessage,Notifiction
from .forms import BuildingForm,UnitForm,TenantForm,LeaseForm,PaymentForm,MaintenanceRequestForm,InvoiceForm,SuppMessageForm

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('rental:supervisor_dashboard')
            elif user.is_tenant:
                return redirect('rental:tenant_dashboard')
        else:
            messages.error(request, "بيانات تسجيل الدخول غير صحيحه.")
    return render(request, 'rental/login.html')

def logout_view(request):
    logout(request)
    return redirect('rental:login')

@login_required
def supervisor_dashboard(request):
    buildings = Building.objects.all()
    tenants = Tenant.objects.all()
    units = Unit.objects.all()
    maintenance_requests = MaintenanceRequest.objects.filter(status='pending')
    return render(request, 'rental/supervisor_dashboard.html', {'buildings': buildings, 'tenants': tenants, 'units': units, 'maintenance_requests': maintenance_requests})

@login_required
def tenant_dashboard(request):
    tenant = get_object_or_404(Tenant, user=request.user)
    leases = Lease.objects.filter(tenant=tenant)
    maintenance_requests = MaintenanceRequest.objects.filter(unit__lease__tenant=tenant)
    invoices = Invoice.objects.filter(lease__tenant=tenant)
    return render(request, 'rental/tenant_dashboard.html', {'tenant': tenant, 'leases': leases, 'maintenance_requests': maintenance_requests, 'invoices': invoices})

class BuildingListView(ListView):
    model = Building
    template_name = 'rental/building_list.html'
    context_object_name = 'buildings'

class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'rental/building_form.html'
    success_url = reverse_lazy('rental:building_list')

class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'rental/building_form.html'
    success_url = reverse_lazy('rental:building_list')

class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'rental/building_confirm_delete.html'
    success_url = reverse_lazy('rental:building_list')

class UnitListView(ListView):
    model = Unit
    template_name = 'rental/unit_list.html'
    context_object_name = 'units'

class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'rental/unit_form.html'
    success_url = reverse_lazy('rental:unit_list')

class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'rental/unit_form.html'
    success_url = reverse_lazy('rental:unit_list')

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'rental/unit_confirm_delete.html'
    success_url = reverse_lazy('rental:unit_list')

class TenantListView(ListView):
    model = Tenant
    template_name = 'rental/tenant_list.html'
    context_object_name = 'tenants'

class TenantCreateView(CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'rental/tenant_form.html'
    success_url = reverse_lazy('rental:tenant_list')

class TenantUpdateView(UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'rental/tenant_form.html'
    success_url = reverse_lazy('rental:tenant_list')

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = 'rental/tenant_confirm_delete.html'
    success_url = reverse_lazy('rental:tenant_list')

class LeaseListView(ListView):
    model = Lease
    template_name = 'rental/lease_list.html'
    context_object_name = 'leases'

class LeaseCreateView(CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/lease_form.html'
    success_url = reverse_lazy('rental:lease_list')

class LeaseUpdateView(UpdateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/lease_form.html'
    success_url = reverse_lazy('rental:lease_list')

class LeaseDeleteView(DeleteView):
    model = Lease
    template_name = 'rental/lease_confirm_delete.html'
    success_url = reverse_lazy('rental:lease_list')

class PaymentListView(ListView):
    model = Payment
    template_name = 'rental/payment_list.html'
    context_object_name = 'payments'

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'rental/payment_form.html'
    success_url = reverse_lazy('rental:payment_list')

class MaintenanceRquestListView(ListView):
    model = MaintenanceRequest
    template_name = 'rental/maintenance_request_list.html'
    context_object_name = 'maintenance_requests'

class MaintenanceRquestCreateView(CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

class InvoceListView(ListView):
    model = Invoice
    template_name = 'rental/invoice_list.html'
    context_object_name = 'invoices'

class InvoceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'rental/invoice_form.html'
    success_url = reverse_lazy('rental:invoice_list')

class SupportMessageListView(ListView):
    model = SupportMessage
    template_name = 'rental/support_message_list.html'
    context_object_name = 'support_messages'

class SupportMessageCreateView(CreateView):
    model = SupportMessage
    form_class = SuppMessageForm
    template_name = 'rental/support_message_form.html'
    success_url = reverse_lazy('rental:support_message_list')

class NotifictionListView(ListView):
    model = Notifiction
    template_name = 'rental/notifiction_list.html'
    context_object_name = 'notifictions'