from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User, Building, Unit, Tenant, Lease, Payment, MaintenanceRequest
from .forms import UserLoginForm, TenantForm, LeaseForm

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('rental:supervisor_dashboard')
                elif user.is_tenant:
                    return redirect('rental:tenant_dashboard')
            else:
                messages.error(request, "بيانات تسجيل الدخول غير صحيحة")
    else:
        form = UserLoginForm()
    return render(request, 'rental/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('rental:login')

def supervisor_dashboard(request):
    building = Building.objects.first()
    units = building.units.all()
    tenants = Tenant.objects.all()
    return render(request, 'rental/supervisor_dashboard.html', {
        'building': building, 
        'units': units, 
        'tenants': tenants,
    })

def tenant_dashboard(request):
    tenant = Tenant.objects.get(user=request.user)
    leases = Lease.objects.filter(tenant=tenant)
    return render(request, 'rental/tenant_dashboard.html', {'tenant': tenant, 'leases': leases})