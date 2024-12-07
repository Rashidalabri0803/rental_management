from django.shortcuts import render, get_object_or_404, redirect
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest
from .forms import UnitForm, TenantForm, LeaseForm, PaymentForm, MaintenanceRequestForm

def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'rental/units/unit_list.html', {'units': units})

def unit_detail(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return render(request, 'rental/units/unit_detail.html', {'unit': unit})

def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'rental/units/unit_form.html', {'form': form})

def edit_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'rental/units/unit_form.html', {'form': form})

def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('unit_list')
    return render(request, 'rental/units/unit_confirm_delete.html', {'unit': unit})

def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'rental/tenants/tenant_list.html', {'tenants': tenants})

def tenant_detail(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    return render(request, 'rental/tenants/tenant_detail.html', {'tenant': tenant})

def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'rental/tenants/tenant_form.html', {'form': form})

def edit_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'rental/tenants/tenant_form.html', {'form': form})

def delete_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    return render(request, 'rental/tenants/tenant_confirm_delete.html', {'tenant': tenant})

def lease_list(request):
    leases = Lease.objects.all()
    return render(request, 'rental/leases/lease_list.html', {'leases': leases})

def lease_detail(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    return render(request, 'rental/leases/lease_detail.html', {'lease': lease})

def add_lease(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lease_list')
    else:
        form = LeaseForm()
    return render(request, 'rental/leases/lease_form.html', {'form': form})

def edit_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            return redirect('lease_list')
    else:
        form = LeaseForm(instance=lease)
    return render(request, 'rental/leases/lease_form.html', {'form': form})

def delete_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        lease.delete()
        return redirect('lease_list')
    return render(request, 'rental/leases/lease_confirm_delete.html', {'lease': lease})

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'rental/payments/payment_list.html', {'payments': payments})

def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'rental/payments/payment_form.html', {'form': form})

def maintenance_request_list(request):
    maintenance_requests = MaintenanceRequest.objects.all()
    return render(request, 'rental/maintenance_requests/maintenance_request_list.html', {'maintenance_requests': maintenance_requests})

def add_maintenance_request(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_request_list')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'rental/maintenance_requests/maintenance_request_form.html', {'form': form})

def edit_maintenance_request(request, pk):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, instance=maintenance_request)
        if form.is_valid():
            form.save()
            return redirect('maintenance_request_list')
    else:
        form = MaintenanceRequestForm(instance=maintenance_request)
    return render(request, 'rental/maintenance_requests/maintenance_request_form.html', {'form': form})