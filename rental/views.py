from django.shortcuts import render, get_object_or_404, redirect
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest
from .forms import UnitForm, TenantForm, LeaseForm, PaymentForm, MaintenanceRequestForm

def unit_list(request):
    units = Unit.objects.all()
    context = {'units': units}
    return render(request, 'units/unit_list.html', context)

def unit_detail(request, pk):
    unit = Unit.objects.get(pk=pk)
    context = {'unit': unit}
    return render(request, 'units/unit_detail.html', context)

def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    context = {'form': form}
    return render(request, 'units/unit_form.html', context)

def unit_update(request, pk):
    unit = Unit.objects.get(pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    context = {'form': form}
    return render(request, 'units/unit_form.html', context)

def unit_delete(request, pk):
    unit = Unit.objects.get(pk=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('unit_list')
    context = {'unit': unit}
    return render(request, 'units/unit_confirm_delete.html', context)

def tenant_list(request):
    tenants = Tenant.objects.all()
    context = {'tenants': tenants}
    return render(request, 'tenants/tenant_list.html', context)

def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    context = {'form': form}
    return render(request, 'tenants/tenant_form.html', context)

def tenant_update(request, pk):
    tenant = Tenant.objects.get(pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    context = {'form': form}
    return render(request, 'tenants/tenant_form.html', context)

def tenant_delete(request, pk):
    tenant = Tenant.objects.get(pk=pk)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    context = {'tenant': tenant}
    return render(request, 'tenants/tenant_confirm_delete.html', context)

def lease_list(request):
    leases = Lease.objects.all()
    context = {'leases': leases}
    return render(request, 'leases/lease_list.html', context)

def lease_create(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lease_list')
    else:
        form = LeaseForm()
    context = {'form': form}
    return render(request, 'leases/lease_form.html', context)

def lease_update(request, pk):
    lease = Lease.objects.get(pk=pk)
    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            return redirect('lease_list')
    else:
        form = LeaseForm(instance=lease)
    context = {'form': form}
    return render(request, 'leases/lease_form.html', context)

def lease_delete(request, pk):
    lease = Lease.objects.get(pk=pk)
    if request.method == 'POST':
        lease.delete()
        return redirect('lease_list')
    context = {'lease': lease}
    return render(request, 'leases/lease_confirm_delete.html', context)

def payment_list(request):
    payments = Payment.objects.all()
    context = {'payments': payments}
    return render(request, 'payments/payment_list.html', context)

def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    context = {'form': form}
    return render(request, 'payments/payment_form.html', context)

def maintenance_request_list(request):
    requests = MaintenanceRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'maintenance_request/maintenance_request_list.html', context)

def maintenance_request_create(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_request_list')
    else:
        form = MaintenanceRequestForm()
    context = {'form': form}
    return render(request, 'maintenance_request/maintenance_request_form.html', context)

def maintenance_request_update(request, pk):
    maintenance_request = MaintenanceRequest.objects.get(pk=pk)
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, instance=maintenance_request)
        if form.is_valid():
            form.save()
            return redirect('maintenance_request_list')
    else:
        form = MaintenanceRequestForm(instance=maintenance_request)
    context = {'form': form}
    return render(request, 'maintenance_request/maintenance_request_form.html', context)
