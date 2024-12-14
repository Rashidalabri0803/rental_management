from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from .models import User, Building, Unit, Tenant, Lease, Payment, Notifiction, MaintenanceRequest, Invoice, ActivityLog
from .forms import BuildingForm, TenantRegistrationForm, UnitForm, LeaseForm, PaymentForm, InvoiceForm, MainenanceRequestForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

class CustomLoginView(LoginView):
    template_name = 'rental/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('rental:supervisor_dashboard')
        elif self.request.user.is_tenant:
            return reverse_lazy('rental:tenant_dashboard')
        return reverse_lazy('rental:home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('rental:login')

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

class LeaseListView(LoginRequiredMixin, ListView):
    model = Lease
    template_name = 'rental/lease_list.html'
    context_object_name = 'leases'

class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/lease_form.html'
    success_url = reverse_lazy('rental:lease_list')

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة العقد بنجاح")
        return super().form_valid(form)

class LeaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Lease
    form_class = LeaseForm
    template_name = 'rental/lease_form.html'
    success_url = reverse_lazy('rental:lease_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث بيانات العقد بنجاح")
        return super().form_valid(form)

class LeaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Lease
    template_name = 'rental/lease_confirm_delete.html'
    success_url = reverse_lazy('rental:lease_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف العقد بنجاح")
        return super().delete(request, *args, **kwargs)

class InvoicesListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'rental/invoice_list.html'
    context_object_name = 'invoices'

class InvoicesCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'rental/invoice_form.html'
    success_url = reverse_lazy('rental:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة الفاتورة بنجاح")
        return super().form_valid(form)

class InvoicesUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'rental/invoice_form.html'
    success_url = reverse_lazy('rental:invoice_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث بيانات الفاتورة بنجاح")
        return super().form_valid(form)

class InvoicesDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'rental/invoice_confirm_delete.html'
    success_url = reverse_lazy('rental:invoice_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف الفاتورة بنجاح")
        return super().delete(request, *args, **kwargs)

class MaitenanceRequestListView(LoginRequiredMixin, ListView):
    model = MaintenanceRequest
    template_name = 'rental/maintenance_request_list.html'
    context_object_name = 'maintenance_requests'

class MaitenanceRequestCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRequest
    form_class = MainenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تمت إضافة طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaitenanceRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRequest
    form_class = MainenanceRequestForm
    template_name = 'rental/maintenance_request_form.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def form_valid(self, form):
        messages.success(self.request, "تم تحديث طلب الصيانة بنجاح")
        return super().form_valid(form)

class MaitenanceRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = MaintenanceRequest
    template_name = 'rental/maintenance_request_confirm_delete.html'
    success_url = reverse_lazy('rental:maintenance_request_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "تم حذف طلب الصيانة بنجاح")
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

class PaymentListView(ListView):
    model = Payment
    template_name = 'rental/payment_list.html'
    context_object_name = 'payments'

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'rental/payment_form.html'
    success_url = reverse_lazy('rental:payment_list')