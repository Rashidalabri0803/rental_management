import builtins
from django.db import models

UNIT_TYPE_CHOICES = [
  ('office', "مكتب"),
  ('apartment', "شقة"),
  ('shop', "محل تجاري"),
]
UNIT_STATUS_CHOICES = [
  ('available', "متاحة"),
  ('rented', "مؤجرة"),
  ('maintenance', "تحت الصيانة"),
]

PAYMENT_METHOD_CHOICES = [
  ('cash', "نقداً"),
  ('bank_transfer', "تحويل بنكي"),
  ('maintenance', "بطاقة ائتمان"),
]

MAINTENANCE_STATUS_CHOICES = [
  ('pending', "قيد الانتظار"),
  ('in_progress', "قيد التنفيذ"),
  ('completed', "مكتملة"),
]

class Unit(models.Model): 
    """يمثل الوحدات السكنية أو التجارية في المبني"""
    unit_number = models.CharField(
      max_length=10,
      unique=True,
      verbose_name="رقم الوحدة"
    )
    unit_type = models.CharField(
      max_length=10,
      choices=UNIT_TYPE_CHOICES,
      verbose_name="نوع الوحدة"
    )
    floor_number = models.PositiveIntegerField(
      verbose_name="رقم الطابق"
    )
    size = models.FloatField(
      verbose_name="المساحة بالمتر المربع"
    )
    rent_price = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="سعر الإيجار الشهري (ريال عماني)"
    )
    status = models.CharField(
      max_length=15,
      choices=UNIT_STATUS_CHOICES,
      default='available',
      verbose_name="حالة الوحدة"
    )
    description = models.TextField(
      blank=True,
      null=True,
      verbose_name="وصف الوحدة"
    )
    created_at = models.DateTimeField(
      auto_now_add=True,
      verbose_name="تاريخ الإضافة"
    )
    updated_at = models.DateTimeField(
      auto_now=True,
      verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "وحدة"
        verbose_name_plural = "الوحدات"
        ordering = ['unit_number']

    def __str__(self):
      return f"وحدة {self.unit_number} - {self.get_unit_type_display()}"


class Tenant(models.Model):
    """يمثل المستأجرين"""
    name = models.CharField(
      max_length=100,
      verbose_name="اسم المستأجر"
    )
    phone_number = models.CharField(
      max_length=15,
      verbose_name="رقم الهاتف"
    )
    email = models.EmailField(
      blank=True,
      null=True,
      verbose_name="البريد الإلكتروني"
    )
    national_id = models.CharField(
      max_length=15,
      unique=True,
      verbose_name="رقم البطاقة المدنية"
    )
    address = models.CharField(
      max_length=255,
      verbose_name="عنوان الإقامة"
    )
    commercial_record = models.CharField(
      max_length=50,
      blank=True,
      null=True,
      verbose_name="رقم السجل التجاري (للوحدات التجارية)"
    )
    notes = models.TextField(
      blank=True,
      null=True,
      verbose_name="ملاحظات إضافية"
    )

    class Meta:
        verbose_name = "مستأجر"
        verbose_name_plural = "المستأجرون"
        ordering = ['name']

    def __str__(self):
        return str(self.name)

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
      Tenant,
      on_delete=models.CASCADE,
      verbose_name="المستأجر"
    )
    start_date = models.DateField(
      verbose_name="تاريخ بداية العقد"
    )
    end_date = models.DateField(
      verbose_name="تاريخ نهاية العقد"
    )
    duration_months = models.PositiveIntegerField(
      verbose_name="مدة العقد (بالشهور)"
    )
    monthly_rent = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="الإيجار الشهري (ريال عماني)"
    )
    deposit = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="المقدم (ريال عماني)"
    )
    contract_file = models.FileField(
      upload_to="contracts",
      blank=True,
      null=True,
      verbose_name="ملف العقد"
    )
    is_active = models.BooleanField(
      default=True,
      verbose_name="العقد نشط"
    )

    class Meta:
        verbose_name = "عقد إيجار"
        verbose_name_plural = "عقود الإيجار"
        ordering = ['start_date']

    def __str__(self):
        return f"عقد {self.contract_number} - {self.unit.unit_number}"

class Payment(models.Model):
    """يمثل المدفوعات"""
    lease = models.ForeignKey(
      Lease,
      on_delete=models.CASCADE,
      verbose_name="عقد الإيجار"
    )
    date = models.DateField(
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
        ordering = ['-date']

    def __str__(self):
        return f"دفعة {self.amount} للعقد {self.lease.contract_number}"

class MaintenanceRequest(models.Model):
    """يمثل طلبات الصيانة"""
    unit = models.ForeignKey(
      Unit,
      on_delete=models.CASCADE,
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
      max_length=20,
      choices=MAINTENANCE_STATUS_CHOICES,
      default='pending',
      verbose_name="حالة الطلب"
    )
    start_date = models.DateField(
      blank=True,
      null=True,
      verbose_name="تاريخ بدء الإصلاح"
    )
    completion_date = models.DateField(
      blank=True,
      null=True,
      verbose_name="تاريخ الإنجاز"
    )
    is_completed = models.BooleanField(
      verbose_name="تم الإنجاز"
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

    def __str__(self):
        return f"طلب صيانة للوحدة {self.unit.unit_number} - {self.get_status_display()}"