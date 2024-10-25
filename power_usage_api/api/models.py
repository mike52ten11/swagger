# api/models.py
from django.db import models

class PowerUser(models.Model):
    electricnumber = models.CharField(max_length=11)
    account = models.CharField(max_length=10)
    registered = models.BooleanField(default=False)
    regdate = models.DateField(null=True, blank=True)

class DeviceData(models.Model):
    DEVICE_CHOICES = [
        ('name1', '設備 1'),
        ('name2', '設備 2'),
        # ('name3', 'Name 3'),
        # 可以根據需要添加更多設備名稱
    ]

    deviceuuid = models.CharField(max_length=36)  # 假設 UUID 是 36 字符長
    name = models.CharField(max_length=10, choices=DEVICE_CHOICES)
    value = models.FloatField()
    datatime = models.BigIntegerField()  # 用於存儲 Unix timestamp
    createtime = models.BigIntegerField()  # 用於存儲 Unix timestamp

    class Meta:
        unique_together = ('deviceuuid', 'name', 'datatime')
        indexes = [
            models.Index(fields=['deviceuuid', 'name']),
            models.Index(fields=['datatime']),
        ]

    def __str__(self):
        return f"The {self.deviceuuid} - {self.name} value of {self.datatime} is {self.value} and the creation date is  {self.createtime}"    



class DeviceElectricNumberMapping(models.Model):
    electricnumber = models.CharField(max_length=11)
    deviceuuid = models.CharField(max_length=36)
    registered = models.BooleanField(default=False)
    createtime = models.DateField(null=True, blank=True)
