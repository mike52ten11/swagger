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

    
    def save(self, *args, **kwargs):
        # 先保存 Device
        super().save(*args, **kwargs)
        
        # 更新相關的綁定記錄
        bands = ElectricNumber_Device_Band.objects.filter(device=self)
        for band in bands:
            band.registered = band.electricnumber.registered and self.registered
            band.save(update_fields=['registered'])

class ElectricNumber(models.Model):


    electricnumber = models.CharField(max_length=11, unique=True)    
    name = models.CharField(max_length=10, default="")
    createtime = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 先保存 Device
        super().save(*args, **kwargs)
        
        # 更新相關的綁定記錄
        bands = ElectricNumber_Device_Band.objects.filter(electricnumber=self)
        print(self.registered)
        for band in bands:
            band.registered = band.electricnumber.registered and self.registered
            band.save(update_fields=['registered'])


class User_Banding_ElectricNumber(models.Model):
    user = models.ForeignKey(
        'User',  # 引用已存在的User模型
        on_delete=models.CASCADE,
        related_name='electric_bindings'
    )
    electricnumber = models.ForeignKey(
        'ElectricNumber',
        on_delete=models.CASCADE,
        related_name='user_bindings'
    )
    account = models.CharField(max_length=10)  # 存儲用戶帳號
    registered = models.BooleanField(default=False)
    regdate = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'electricnumber')  # 確保用戶和電號的綁定是唯一的
    
    def clean(self):
        # 檢查用戶是否是管理員
        if self.user.is_staff or self.user.is_superuser:
            raise ValidationError('Administrator cannot bind electric numbers')
            
        # 檢查是否已達到最大綁定數量（假設最大是5個）
        existing_bindings = User_Banding_ElectricNumber.objects.filter(user=self.user).count()
        if not self.pk and existing_bindings >= 5:
            raise ValidationError('Maximum number of electric number bindings reached')
    
    def save(self, *args, **kwargs):
        if not self.pk:  # 只在創建新記錄時執行
            self.account = self.user.username  # 自動設置user
        
        # 更新registered狀態
        self.registered = (self.electricnumber.registered and 
                         self.user.is_active)
        
        super().save(*args, **kwargs)



class ElectricNumber_Device_Band(models.Model):
    # 使用 ForeignKey 建立關聯，這樣就只能選擇既有的資料
    electricnumber  = models.ForeignKey(
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

    def clean(self):
        # 檢查是否已經存在相關的綁定
        if not self.pk:  # 只在創建新記錄時檢查
            existing_electric = ElectricNumber_Device_Band.objects.filter(
                electricnumber=self.electricnumber
            ).exists()
            
            existing_device = ElectricNumber_Device_Band.objects.filter(
                device=self.device
            ).exists()
            
            if existing_electric:
                raise ValidationError({
                    'electric': f'This electric number  is already bound to another device.'
                })
            
            if existing_device:
                raise ValidationError({
                    'device': f'This device  is already bound to another electric number.'
                })

    def save(self, *args, **kwargs):
        self.clean()
        self.registered = self.electricnumber.registered and self.device.registered
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.electricnumber.electricnumber} - {self.device.deviceuuid}"


class AMIData(models.Model):

    deviceuuid = models.CharField(max_length=36)  # 假設 UUID 是 36 字符長
    name = models.CharField(max_length=10, null=True, blank=True)
    value = models.FloatField()
    datatime = models.BigIntegerField()  # 用於存儲 Unix timestamp
    createtime = models.DateTimeField(auto_now_add=True)  # 用於存儲 Unix timestamp

    class Meta:
        unique_together = ('deviceuuid', 'name', 'datatime')
        indexes = [
            models.Index(fields=['deviceuuid', 'name']),
            models.Index(fields=['datatime']),
        ]

    def __str__(self):
        return f"The {self.deviceuuid} - {self.name} value of {self.datatime} is {self.value} and the creation date is  {self.createtime}"    
