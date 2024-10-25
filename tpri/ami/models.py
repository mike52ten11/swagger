# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

# 當用戶創建時自動生成Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PowerUser(models.Model):
    electricnumber = models.CharField(max_length=11)
    account = models.CharField(max_length=10)
    registered = models.BooleanField(default=False)
    regdate = models.DateField(null=True, blank=True)




class Device(models.Model):
    # DEVICE_CHOICES = [
    #     ('name1', '設備 1'),
    #     ('name2', '設備 2'),
    #     # ('name3', 'Name 3'),
    #     # 可以根據需要添加更多設備名稱
    # ]

    deviceuuid = models.CharField(max_length=36)  # 假設 UUID 是 36 字符長
    
    name = models.CharField(max_length=10)
    createtime = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=True)

    class Meta:
        unique_together = ('deviceuuid', 'name')



class ElectricNumber(models.Model):


    electricnumber = models.CharField(max_length=11, unique=True)    
    name = models.CharField(max_length=10, default="")
    createtime = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=True)


class ElectricNumber_Device_Band(models.Model):
    # 使用 ForeignKey 建立關聯，這樣就只能選擇既有的資料
    electric = models.ForeignKey(
        ElectricNumber,
        on_delete=models.CASCADE,
        related_name='device_bands'
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='electric_bands'
    )
    createtime = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField()

    def save(self, *args, **kwargs):
        # 在儲存前計算 registered 的值（AND 邏輯）
        self.registered = self.electric.registered and self.device.registered
        # 執行模型驗證
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        # 額外的驗證邏輯
        if not self.electric_id or not self.device_id:
            raise ValidationError('Both electric and device must be selected')

    class Meta:
        # 確保 electric 和 device 的組合是唯一的
        unique_together = ('electric', 'device')