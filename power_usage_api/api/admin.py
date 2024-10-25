from django.contrib import admin
from .models import (   PowerUser, 
                        DeviceData, 
                        ElectricNumber
                    )
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

@admin.register(PowerUser)
class PowerUserAdmin(admin.ModelAdmin):
    list_display = ['electricnumber', 'account', 'registered', 'regdate']
    search_fields = ['electricnumber', 'account']

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['deviceuuid', 'name', 'value', 'createtime']
    list_filter = ['name']
    search_fields = ['deviceuuid']
# Register your models here.

@admin.register(Token)
class CustomTokenAdmin(TokenAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


   