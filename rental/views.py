from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User, Building, Unit, Tenant, Lease, SupervisorPermission, UnitType, Payment, MaintenanceRequest
from .forms import BuildingForm, UnitForm, TenantForm, LeaseForm, SupervisorPermissionForm, UnitTypeForm

class SupervisorPermissionListView(ListView):
    model = SupervisorPermission
    template_name = 'rental/supervisor_permissions/permissions_list.html'
    context_object_name = 'permissions'

class SupervisorPermissionCreatView(CreateView):
    model = SupervisorPermission
    form_class = SupervisorPermissionForm
    template_name = 'rental/supervisor_permissions/permissions_form.html'
    success_url = '/supervisor/permissions/'

class SupervisorPermissionUpdateView(UpdateView):
    model = SupervisorPermission
    form_class = SupervisorPermissionForm
    template_name = 'rental/supervisor_permissions/permissions_form.html'
    success_url = '/supervisor/permissions/'

class SupervisorPermissionDeleteView(DeleteView):
    model = SupervisorPermission
    template_name = 'rental/supervisor_permissions/permissions_confirm_delete.html'
    success_url = '/supervisor/permissions/'

class UnitTypeListView(ListView):
    model = UnitType
    template_name = 'rental/unit_types/unit_types_list.html'
    context_object_name = 'unit_types'

class UnitTypeCreatView(CreateView):
    model = UnitType
    form_class = UnitTypeForm
    template_name = 'rental/unit_types/unit_types_form.html'
    success_url = '/unit-types/'

class UnitTypeUpdateView(UpdateView):
    model = UnitType
    form_class = UnitTypeForm
    template_name = 'rental/unit_types/unit_types_form.html'
    success_url = '/unit-types/'

class LeasetListView(ListView):
    model = Lease
    template_name = 'rental/leases/leases_list.html'
    context_object_name = 'leases'

class LeaseCreatView(CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/leases/leases_form.html'
    success_url = '/leases/'

class LeaseUpdateView(UpdateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/leases/leases_form.html'
    success_url = '/leases/'

class LeaseDeleteView(DeleteView):
    model = Lease
    template_name = 'rental/leases/leases_confirm_delete.html'
    success_url = '/leases/'