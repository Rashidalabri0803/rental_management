from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

TENANT_TYPE_CHOICES = [
  ('Individual', "شخصي"),
  ('Company', "شركة"),
]
STATUS_CHOICES = [
    ('pending', "قيد الانتظار"),
    ('in_progress', "تحت التنفيذ"),
    ('completed', "مكتملة"),
    ('rejected', "مرفوضة"),
  ]
UNIT_STATUS_CHOICES = [
  ('available', "متاحة"),
  ('rented', "مؤجرة"),
  ('maintenance', "تحت الصيانة"),
]

LEASE_STATUS_CHOICES = [
  ('active', "نشط"),
  ('expired', "منتهي"),
  ('suspended', "معلق"),
]

PAYMENT_METHOD_CHOICES = [
  ('cash', "نقداً"),
  ('bank_transfer', "تحويل بنكي"),
  ('maintenance', "بطاقة ائتمان"),
]

NOTIFICTION_TYPE_CHOICES = [
  ('payment_due', "إشعار مستحقات"),
  ('maintenance_update', "تحديث صيانة"),
  ('lease_update', "تحديث عقد"),
]

class User(AbstractUser):
  phone_number = models.CharField(
    max_length=15, 
    unique=True, 
    verbose_name="رقم الهاتف",
    help_text="يجب أن يكون رقم الهاتف فريداً",
  )
  email = models.EmailField(
    unique=True,
    verbose_name="البريد الإلكتروني",
    help_text="يجب أن يكون البريد الإلكتروني فريداً",
  )
  is_tenant = models.BooleanField(
    default=False, 
    verbose_name="هل هو مستأجر؟",
  )
  is_supervisor = models.BooleanField(
    default=False, 
    verbose_name="هل هو مشرف؟",
  )

  def __str_(self):
    return self.username
    
class Building(models.Model):
  name = models.CharField(
    max_length=100,
    unique=True,
    verbose_name="اسم المبني",
  )
  location = models.TextField(
    verbose_name="موقع المبني",
  )
  total_units = models.PositiveIntegerField(
    verbose_name="إجمالي الوحدات",
  )
  address = models.CharField(
    max_length=255,
    verbose_name="عنوان المبني",
    blank=True,
    null=True,
  )
  created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name="تاريخ الإضافة",
  )
  updated_at = models.DateTimeField(
    auto_now=True,
    verbose_name="تاريخ التحديث",
  )

  class Meta:
    verbose_name = "مبنى"
    verbose_name_plural = "المباني"

  def __str_(self):
    return self.name

  def get_rented_units(self):
    return self.units.filter(status='rented').count()

  def get_available_units(self):
    return self.units.filter(status='available').count()

class Unit(models.Model): 
  """يمثل الوحدات السكنية أو التجارية في المبني"""
  building = models.ForeignKey(
    Building,
    on_delete=models.CASCADE,
    related_name="units",
    verbose_name="المبني",
  )
  unit_number = models.CharField(
    max_length=10,
    unique=True,
    verbose_name="رقم الوحدة"
  )
  unit_type = models.CharField(
    max_length=50,
    verbose_name="نوع الوحدة",
  )
  size = models.FloatField(
    verbose_name="المساحة (متر مربع)"
  )
  floor_number = models.PositiveIntegerField(
    verbose_name="رقم الطابق"
  )
  rent_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="سعر الإيجار (ريال عماني)"
  )
  status = models.CharField(
    max_length=15,
    choices=UNIT_STATUS_CHOICES,
    default="available",
    verbose_name="حالة الوحدة"
  )
  description = models.TextField(
    blank=True,
    null=True,
    verbose_name="وصف الوحدة"
  )

  class Meta:
      verbose_name = "وحدة"
      verbose_name_plural = "الوحدات"
      ordering = ['unit_number']

  def __str_(self):
    return f"وحدة {self.unit_number} - {self.building.name}"

class Lease(models.Model):
  """يمثل عقود الإيجار"""
  contract_number = models.CharField(
    max_length=20,
    unique=True,
    verbose_name="رقم العقد"
  )
  unit = models.OneToOneField(
    Unit,
    on_delete=models.CASCADE,
    verbose_name="الوحدة"
  )
  tenant = models.ForeignKey(
    'Tenant',
    on_delete=models.CASCADE,
    verbose_name="المستأجر"
  )
  start_date = models.DateField(
    verbose_name="تاريخ بداية العقد"
  )
  end_date = models.DateField(
    verbose_name="تاريخ نهاية العقد"
  )
  monthly_rent = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="الإيجار الشهري (ريال عماني)"
  )
  deposit = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="مقدم (ريال عماني)"
  )
  discount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="الخصم (ريال عماني)"
  )
  status = models.CharField(
    max_length=10,
    choices=LEASE_STATUS_CHOICES,
    default="active",
    verbose_name="حالة العقد"
  )
  is_active = models.BooleanField(
    default=True,
    verbose_name="العقد نشط"
  )

  class Meta:
      verbose_name = "عقد إيجار"
      verbose_name_plural = "عقود الإيجار"
      ordering = ['start_date']

  def __str_(self):
      return f"عقد {self.contract_number} - {self.unit.unit_number}"

  def get_remaining_days(self):
    return (self.end_date - date.today()).days if self.end_date else 0

  def clean(self):
    if self.start_date and self.end_date and self.start_date > self.end_date:
      raise ValidationError("تاريخ البداية يجب أن يكون قبل تاريخ النهاية.")

class Tenant(models.Model):
  """يمثل المستأجرين"""
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    verbose_name="حساب المستخدم"
  )
  tenant_type = models.CharField(
    max_length=10,
    choices=TENANT_TYPE_CHOICES,
    verbose_name="نوع المستأجر"
  )
  national_id = models.CharField(
    max_length=20,
    unique=True,
    verbose_name="رقم البطاقة المدنية / السجل التجاري"
  )
  company_name = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    verbose_name="اسم الشركة"
  )
  address = models.CharField(
    max_length=255,
    verbose_name="عنوان الإقامة أو الشركة"
  )
  notes = models.TextField(
    blank=True,
    null=True,
    verbose_name="ملاحظات إضافية"
  )

  class Meta:
      verbose_name = "مستأجر"
      verbose_name_plural = "المستأجرون"

  def __str_(self):
      return self.user.username

class Notifiction(models.Model):
  """يمثل الإشعارات"""
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name="notifications",
      verbose_name="المستخدم"
  )
  message = models.TextField(
      verbose_name="نص الإشعار"
  )
  created_at = models.DateTimeField(
      auto_now_add=True,
      verbose_name="تاريخ الإشعار"
  )
  read = models.BooleanField(
      default=False,
      verbose_name="تمت القراءة"
  )

  class Meta:
      verbose_name = "إشعار"
      verbose_name_plural = "الإشعارات"
      ordering = ['-created_at']

  def __str_(self):
      return f"إشعار للمستخدم {self.user.username}"

@receiver(post_save, sender=Lease)
def create_notifiction_on_lease(sender, instance, created, **kwargs):
  if created:
    Notifiction.objects.create(
      user=instance.tenant.user,
      message=f"تم إنشاء عقد إيجار جديد: {instance.unit.unit_number}",
    )

class MaintenanceRequest(models.Model):
  """يمثل طلبات الصيانة"""
  unit = models.ForeignKey(
    Unit,
    on_delete=models.CASCADE,
    related_name="maintenance_requests",
    verbose_name="الوحدة"
  )
  description = models.TextField(
    verbose_name="وصف المشكلة"
  )
  request_date = models.DateField(
    auto_now_add=True,
    verbose_name="تاريخ الطلب"
  )
  status = models.CharField(
    max_length=15,
    choices=STATUS_CHOICES,
    default='pending',
    verbose_name="حالة الطلب"
  )
  notes = models.TextField(
    blank=True,
    null=True,
    verbose_name="ملاحظات إضافية"
  )

  class Meta:
      verbose_name = "طلب الصيانة"
      verbose_name_plural = "طلبات الصيانة"
      ordering = ['-request_date']

  def __str_(self):
      return f"طلب صيانة للوحدة {self.unit.unit_number} - {self.get_status_display()}"

class Invoice(models.Model):
  STATUS_CHOICES = [
    ('unpaid', "غير مدفوعة"),
    ('paid', "مدفوعة"),
    ('overdue', "متأخرة"),
  ]
  invoice_number = models.CharField(
    max_length=20,
    unique=True,
    verbose_name="رقم الفاتورة"
  )
  lease = models.ForeignKey(
    Lease,
    on_delete=models.CASCADE,
    related_name="invoices",
    verbose_name="عقد الإيجار"
  )
  issue_date = models.DateField(
    auto_now_add=True,
    verbose_name="تاريخ الإصدار"
  )
  due_date = models.DateField(
    verbose_name="تاريخ الاستحقاق"
  )
  total_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="إجمالي المبلغ (ريال عماني)"
  )
  status = models.CharField(
    max_length=10,
    choices=STATUS_CHOICES,
    default='unpaid',
    verbose_name="حالة الفاتورة"
  )

  class Meta:
      verbose_name = "فاتورة"
      verbose_name_plural = "الفواتير"
      ordering = ['-issue_date']

  def __str_(self):
      return f"فاتورة {self.invoice_number} - {self.lease.contract_number}"

  def is_overdues(self):
    return self.due_date < date.today() and self.status != 'paid'

  def mark_as_paid(self):
    self.status = 'paid'
    self.save()

class ActivityLog(models.Model):
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      null=True,
      verbose_name="المستخدم"
  )
  action = models.CharField(
      max_length=255,
      verbose_name="النشاط"
  )
  timestamp = models.DateTimeField(
      auto_now_add=True,
      verbose_name="التاريخ والوقت"
  )
  details = models.TextField(
      blank=True,
      null=True,
      verbose_name="تفاصيل إضافية"
  )

  class Meta:
      verbose_name = "سجل النشاط"
      verbose_name_plural = "سجلات الأنشطة"
      ordering = ['-timestamp']

  def __str_(self):
      return f"نشاط بواسطة {self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Payment(models.Model):
    """يمثل المدفوعات"""
    lease = models.ForeignKey(
      Lease,
      on_delete=models.CASCADE,
      related_name="payments",
      verbose_name="عقد الإيجار"
    )
    payment_date = models.DateField(
      auto_now_add=True,
      verbose_name="تاريخ الدفع"
    )
    amount = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="المبلغ المدفوع (ريال عماني)"
    )
    payment_method = models.CharField(
      max_length=20,
      choices=PAYMENT_METHOD_CHOICES,
      verbose_name="طريقة الدفع"
    )
    notes = models.TextField(
      blank=True,
      null=True,
      verbose_name="ملاحظات"
    )

    class Meta:
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"
        ordering = ['-payment_date']

    def __str_(self):
        return f"مدفوعات العقد {self.lease.contract_number} - {self.amount} ريال عماني"
      