from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Building, Unit, Tenant, Supervisor, Lease, Payment, MaintenanceRequest
from .forms import BuildingForm, UnitForm, TenantForm, SupervisorForm, LeaseForm, PaymentForm, MaintenanceRequestForm

class BuildingListView(ListView):
    model = Building
    template_name = "rental/buildings/building_list.html"
    context_object_name = "buildings"
    ordering = ["name"]
    paginate_by = 10

class BuildingCrateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = "rental/buildings/building_form.html"
    success_url = reverse_lazy("rental:building_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة المبنى بنجاح")
        return super().form_valid(form)

class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = "rental/buildings/building_form.html"
    success_url = reverse_lazy("rental:building_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل بيانات المبنى بنجاح")
        return super().form_valid(form)

class BuildingDeleteView(DeleteView):
    model = Building
    template_name = "rental/buildings/building_confirm_delete.html"
    success_url = reverse_lazy("rental:building_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف المبنى بنجاح")
        return super().delete(request, *args, **kwargs)

class UnitListView(ListView):
    model = Unit
    template_name = "rental/units/unit_list.html"
    context_object_name = "units"
    ordering = ["unit_number"]
    paginate_by = 10
        
class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "rental/units/unit_form.html"
    success_url = reverse_lazy("rental:unit_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة الوحدة بنجاح.")
        return super().form_valid(form)

class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "rental/units/unit_form.html"
    success_url = reverse_lazy("rental:unit_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل بيانات الوحدة بنجاح.")
        return super().form_valid(form)
        
class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "rental/units/unit_confirm_delete.html"
    success_url = reverse_lazy("rental:unit_list")

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
    success_url = reverse_lazy("rental:tenant_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة المستأجر بنجاح.")
        return super().form_valid(form)

class TenantUpdateView(UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = "rental/tenants/tenant_form.html"
    success_url = reverse_lazy("rental:tenant_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل بيانات المستأجر بنجاح.")
        return super().form_valid(form)

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = "rental/tenants/tenant_confirm_delete.html"
    success_url = reverse_lazy("rental:tenant_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف المستأجر بنجاح.")
        return super().delete(request, *args, **kwargs)

class SupervisorListView(ListView):
    model = Supervisor
    template_name = "rental/supervisors/supervisor_list.html"
    context_object_name = "supervisors"
    ordering = ['user__username']
    paginate_by = 10

class SupervisorCreateView(CreateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = "rental/supervisors/supervisor_form.html"
    success_url = reverse_lazy("rental:supervisor_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة المشرف بنجاح.")
        return super().form_valid(form)

class SupervisorUpdateView(UpdateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = "rental/supervisors/supervisor_form.html"
    success_url = reverse_lazy("rental:supervisor_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل بيانات المشرف بنجاح.")
        return super().form_valid(form)

class SupervisorDeleteView(DeleteView):
    model = Supervisor
    template_name = "rental/supervisors/supervisor_confirm_delete.html"
    success_url = reverse_lazy("rental:supervisor_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف المشرف بنجاح.")
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
    success_url = reverse_lazy("rental:lease_list")

    def form_valid(self, form):
        messages.success(self.request, "تم إنشاء عقد الإيجار بنجاح.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "حدث خطأ أثناء إنشاء العقد. يرجى التحقق من البيانات المدخلة")
        return super().form_invalid(form)
        

class PaymentListView(ListView):
    model = Payment
    template_name = "rental/payments/payment_list.html"
    ordering = ['-date']
    paginate_by = 10

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "rental/payments/payment_form.html"
    success_url = reverse_lazy("rental:payment_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تسجيل الدفعة بنجاح.")
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
    success_url = reverse_lazy("rental:maintenance_request_list")

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة طلب الصيانة بنجاح.")
        return super().form_valid(form)

class MaintenanceRequestUpdateView(UpdateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "rental/maintenance_requests/maintenance_request_form.html"
    success_url = reverse_lazy("rental:maintenance_request_list")

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل طلب الصيانة بنجاح.")
        return super().form_valid(form)