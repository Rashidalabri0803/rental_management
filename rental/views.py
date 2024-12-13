from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from .models import User, Building, Unit, Tenant, Lease, Payment, Notifiction, MaintenanceRequest, Invoice, ActivityLog
from .forms import BuildingForm, TenantRegistrationForm, UnitForm, LeaseForm, PaymentForm, InvoiceForm, MainenanceRequestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

class TenantRegistrationView(CreateView):
    model = User
    form_class = TenantRegistrationForm
    template_name = 'rental/tenant_registration.html'
    success_url = reverse_lazy('rental:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_tenant = True
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "تم تسجيل المستأجر بنجاح. يمكنك تسجيل الدخول الآن.")
        return super().form_valid(form)

class SupervisorDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lease
    template_name = 'rental/supervisor_dashboard.html'
    context_object_name = 'leases'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buildings'] = Building.objects.all()
        context['units'] = Unit.objects.all()
        context['active_leases'] = Lease.objects.filter(is_active=True)
        context['pending_maintenance'] = MaintenanceRequest.objects.filter(status='pending')
        return context

class TenantDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lease
    template_name = 'rental/tenant_dashboard.html'
    context_object_name = 'leases'

    def test_func(self):
        return self.request.user.is_tenant

    def get_queryset(self):
        return Lease.objects.filter(tenant__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoices'] = Invoice.objects.filter(lease__tenant__user=self.request.user)
        context['maintenance_requests'] = MaintenanceRequest.objects.filter(unit__lease__tenant__user=self.request.user)
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
    form_class = MainenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تم إرسال طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaintenanceRquestUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRequest
    form_class = MainenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaintenanceRquestDeleteView(LoginRequiredMixin, DeleteView):
    model = MainenanceRequestForm
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