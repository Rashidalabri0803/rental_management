from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Unit, Tenant, Lease, Payment, MaintenanceRequest
from .forms import UnitForm, TenantForm, LeaseForm, PaymentForm, MaintenanceRequestForm

class UnitListView(ListView):
    model = Unit
    template_name = "rental/units/unit_list.html"
    context_object_name = "units"
    ordering = ['unit_number']
    paginate_by = 10

class UnitDetailView(DetailView):
    model = Unit
    template_name = "rental/units/unit_detail.html"
    context_object_name = "unit"

class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "rental/units/unit_form.html"
    success_url = reverse_lazy("unit_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة الوحدة بنجاح.")
        return super().form_valid(form)

class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "rental/units/unit_form.html"
    success_url = reverse_lazy("unit_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل الوحدة بنجاح.")
        return super().form_valid(form)

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "rental/units/unit_confirm_delete.html"
    success_url = reverse_lazy("unit_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف الوحدة بنجاح.")
        return super().delete(request, *args, **kwargs)

class TenantListView(ListView):
    model = Tenant
    template_name = "rental/tenants/tenant_list.html"
    context_object_name = "tenants"
    ordering = ['name']
    paginate_by = 10

class TenantCreateView(CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = "rental/tenants/tenant_form.html"
    success_url = reverse_lazy("tenant_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة المستأجر بنجاح.")
        return super().form_valid(form)

class TenantUpdateView(UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = "rental/tenants/tenant_form.html"
    success_url = reverse_lazy("tenant_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل بيانات المستأجر بنجاح.")
        return super().form_valid(form)

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = "rental/tenants/tenant_confirm_delete.html"
    success_url = reverse_lazy("tenant_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف المستأجر بنجاح.")
        return super().delete(request, *args, **kwargs)

class LeaseListView(ListView):
    model = Lease
    template_name = "rental/leases/lease_list.html"
    context_object_name = "leases"
    ordering = ['-start_date']
    paginate_by = 10

class LeaseCreateView(CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = "rental/leases/lease_form.html"
    success_url = reverse_lazy("lease_list")

    def form_valid(self, form):
        messages.success(self.request, "تم إنشاء عقد الإيجار بنجاح.")
        return super().form_valid(form)

class LeaseUpdateView(UpdateView):
    model = Lease
    form_class = LeaseForm
    template_name = "rental/leases/lease_form.html"
    success_url = reverse_lazy("lease_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل عقد الإيجار بنجاح.")
        return super().form_valid(form)

class LeaseDeleteView(DeleteView):
    model = Lease
    template_name = "rental/leases/lease_confirm_delete.html"
    success_url = reverse_lazy("lease_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف عقد الإيجار بنجاح.")
        return super().delete(request, *args, **kwargs)

class PaymentListView(ListView):
    model = Payment
    template_name = "rental/payments/payment_list.html"
    ordering = ['-date']
    paginate_by = 10

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "rental/payments/payment_form.html"
    success_url = reverse_lazy("payment_list")

    def form_valid(self, form):
        messages.success(self.request, "تم إضافة دفعة بنجاح.")
        return super().form_valid(form)

class MaintenanceRequestListView(ListView):
    model = MaintenanceRequest
    template_name = "rental/maintenance_requests/maintenance_request_list.html"
    ordering = ['-request_date']
    paginate_by = 10

class MaintenanceRequestCreateView(CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "rental/maintenance_requests/maintenance_request_form.html"
    success_url = reverse_lazy("maintenance_request_list")

    def form_valid(self, form):
        messages.success(self.request, "تم إنشاء طلب الصيانة بنجاح.")
        return super().form_valid(form)

class MaintenanceRequestUpdateView(UpdateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "rental/maintenance_requests/maintenance_request_form.html"
    success_url = reverse_lazy("maintenance_request_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل طلب الصيانة بنجاح.")
        return super().form_valid(form)