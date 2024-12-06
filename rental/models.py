import builtins
from django.db import models

class Unit(models.Model):
    UNIT_TYPE_CHOICES = [
        ('office', 'مكتب'),
        ('apartment', 'شقة'),
        ('shop', 'محل'),
    ]
    unit_number = models.CharField(
      max_length=10,
      unique=True,
      verbose_name='رقم الوحدة'
    )
    unit_type = models.CharField(
      max_length=10,
      choices=UNIT_TYPE_CHOICES,
      verbose_name="نوع الوحدة"
    )
    size = models.FloatField(
      verbose_name="المساحة بالمتر المربع"
    )
    rent_price = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="سعر الإيجار الشهري"
    )
    is_available = models.BooleanField(
      verbose_name="متاح"
    )
    description = models.TextField(
      blank=True,
      null=True,
      verbose_name="وصف الوحدة"
    )

    class Meta:
        verbose_name = "وحدة"
        verbose_name_plural = "الوحدات"

    def __str__(self):
      return f"{dict(self.UNIT_TYPE_CHOICES).get(self.unit_type)} {self.unit_number}"


class Tenant(models.Model):
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
      max_length=50,
      unique=True,
      verbose_name="رقم الهوية الوطنية"
    )
    address = models.CharField(
      max_length=255,
      verbose_name="العنوان"
    )

    class Meta:
        verbose_name = "مستأجر"
        verbose_name_plural = "المستأجرون"

    def __str__(self):
        return str(self.name)

class Lease(models.Model):
    unit = models.ForeignKey(
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
    monthly_rent = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="الإيجار الشهري"
    )
    deposit = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="المقدم"
    )
    contract_file = models.FileField(
      upload_to="contracts",
      blank=True,
      null=True,
      verbose_name="ملف العقد"
    )

    class Meta:
        verbose_name = "عقد إيجار"
        verbose_name_plural = "عقود الإيجار"

    def __str__(self):
        return f"عقد إيجار {self.unit} - {self.tenant}"

class Payment(models.Model):
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
      verbose_name="المبلغ المدفوع"
    )
    payment_method = models.CharField(
      max_length=50,
      choices=[
        ('cash', 'كاش'),
        ('credit_card', 'بطاقة الائتمان'),
        ('check', 'شيك'),
      ],
      verbose_name="طريقة الدفع"
    )
    description = models.TextField(
      blank=True,
      null=True,
      verbose_name="ملاحظات"
    )

    class Meta:
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"

    def __str__(self):
        return f"دفعة {self.amount} للعقد {self.lease}"

class MaintenanceRequest(models.Model):
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
    completion_date = models.DateField(
      blank=True,
      null=True,
      verbose_name="تاريخ الإنجاز"
    )
    is_completed = models.BooleanField(
      verbose_name="تم الإنجاز"
    )

    class Meta:
        verbose_name = "طلب الصيانة"
        verbose_name_plural = "طلبات الصيانة"

    def __str__(self):
        return f"صيانة - {self.unit}"