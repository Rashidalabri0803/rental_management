from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from .models import User, Building, Supervisor, Unit, UnitType, Tenant, Lease, Payment, Notifiction, MaintenanceRequest, Invoice, ActivityLog
from .forms import UserForm, BuildingForm, SupervisorForm, UnitForm, UnitTypeForm, TenantForm, LeaseForm, PaymentForm, NotifictionForm, MaintenanceRequestForm, InvoiceForm, ActivityLogForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, username=phone_number, password=password)
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
    messages.success(request, "تم تسجيل الخروج بنجاح.")
    return redirect('rental:login')

class SupervisorDashboardView(LoginRequiredMixin, ListView):
    template_name = 'rental/supervisor_dashboard.html'
    context_object_name = 'dashboard_data'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buildings'] = Building.objects.all()
        context['units'] = Unit.objects.all()
        context['tenants'] = Tenant.objects.all()
        context['active_leases'] = Lease.objects.filter(is_active=True)
        context['pending_maintenance'] = MaintenanceRequest.objects.filter(status='pending')
        return context

class TenantDashboardView(LoginRequiredMixin, ListView):
    template_name = 'rental/tenant_dashboard.html'
    context_object_name = 'dashboard_data'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = get_object_or_404(Tenant, user=self.request.user)
        context['leases'] = Lease.objects.filter(tenant=tenant)
        context['maintenance_requests'] = MaintenanceRequest.objects.filter(unit__lease__tenant=tenant)
        context['payments'] = Payment.objects.filter(lease__tenant=tenant)
        context['notifications'] = Notifiction.objects.filter(user=self.request.user, read=False)
        return context

class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'rental/building_list.html'
    context_object_name = 'buildings'

class BuildingCreateView(LoginRequiredMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'rental/building_form.html'
    success_url = reverse_lazy('rental:building_list')

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة المبني بنجاح")
        return super().form_valid(form)

class BuildingUpdateView(LoginRequiredMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'rental/building_form.html'
    success_url = reverse_lazy('rental:building_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث بيانات المبني بنجاح")
        return super().form_valid(form)
        
class BuildingDeleteView(LoginRequiredMixin, DeleteView):
    model = Building
    template_name = 'rental/building_confirm_delete.html'
    success_url = reverse_lazy('rental:building_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف المبني بنجاح")
        return super().delete(request, *args, **kwargs)

class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'rental/unit_list.html'
    context_object_name = 'units'

class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'rental/unit_form.html'
    success_url = reverse_lazy('rental:unit_list')

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة الوحدة بنجاح")
        return super().form_valid(form)

class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'rental/unit_form.html'
    success_url = reverse_lazy('rental:unit_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث بيانات الوحدة بنجاح")
        return super().form_valid(form)

class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'rental/unit_confirm_delete.html'
    success_url = reverse_lazy('rental:unit_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف الوحدة بنجاح")
        return super().delete(request, *args, **kwargs)

class NoitificationListView(LoginRequiredMixin, ListView):
    model = Notifiction
    template_name = 'rental/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notifiction.objects.filter(user=self.request.user)

@login_required
def mark_notifiction_as_read(request, pk):
    notifiction = get_object_or_404(Notifiction, pk=pk, user=request.user)
    notifiction.read = True
    notifiction.save()
    messages.success(request, "تم تعليم الإشعار كمقروء.")
    return redirect('rental:notifiction_list')

class MaintenanceRquestListView(LoginRequiredMixin, ListView):
    model = MaintenanceRequest
    template_name = 'rental/maintenance_request_list.html'
    context_object_name = 'maintenance_requests'
    ordering = ['-request_date']

    def get_queryset(self):
        if slef.request.user.is_superuser:
            return MaintenanceRequest.objects.all()
        elif self.request.user.is_tenant:
            tenant_units = Unit.objects.filter(lease__tenant=self.request.user)
            return MaintenanceRequest.objects.filter(unit__in=tenant_units)
        return MaintenanceRequest.objects.none()

class MaintenanceRquestCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تم إرسال طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaintenanceRquestUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaintenanceRquestDeleteView(LoginRequiredMixin, DeleteView):
    model = MaintenanceRequest
    template_name = 'rental/maintenance_request_confirm_delete.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف طلب الصيانة بنجاح")
        return super().delete(request, *args, **kwargs)

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'rental/invoice_list.html'
    context_object_name = 'invoices'
    ordering = ['-invoice_date']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Invoice.objects.all()
        elif self.request.user.is_tenant:
            tenant_leases = Lease.objects.filter(tenant__user=self.request.user)
        return Invoice.objects.none()

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'rental/invoice_form.html'
    success_url = reverse_lazy('rental:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, "تم إنشاء فاتورة بنجاح")
        return super().form_valid(form)

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'rental/invoice_form.html'
    success_url = reverse_lazy('rental:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث فاتورة بنجاح")
        return super().form_valid(form)

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'rental/invoice_confirm_delete.html'
    success_url = reverse_lazy('rental:invoice_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف فاتورة بنجاح")
        return super().delete(request, *args, **kwargs)

class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'rental/activity_log_list.html'
    context_object_name = 'activity_logs'
    ordering = ['-timestamp']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ActivityLog.objects.all()
        return ActivityLog.objects.filter(user=self.request.user)

class ActivityLogCreateView(LoginRequiredMixin, CreateView):
    model = ActivityLog
    form_class = ActivityLogForm
    template_name = 'rental/activity_log_form.html'
    success_url = reverse_lazy('rental:activity_log_list')

    def form_valid(self, form):
        messages.success(self.request, "تم إضافة سجل النشاط بنجاح")
        return super().form_valid(form)
    
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