from django.contrib import admin
from .models import (   User, 
                        PowerUser, 
                        Device, 
                        ElectricNumber, 
                        ElectricNumber_Device_Band
                    )
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']


@admin.register(PowerUser)
class PowerUserAdmin(admin.ModelAdmin):
    list_display = ['electricnumber', 'account', 'registered', 'regdate']
    search_fields = ['electricnumber', 'account']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['deviceuuid', 'name', 'createtime']
    list_filter = ['name']
    search_fields = ['deviceuuid']

@admin.register(ElectricNumber)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['electricnumber', 'name']
    list_filter = ['electricnumber']
    search_fields = ['electricnumber'] 


@admin.register(ElectricNumber_Device_Band)
class ElectricNumber_Device_Band_Admin(admin.ModelAdmin):
    list_display = ('electric_name', 'device_name', 'registered', 'createtime')
    list_filter = ('registered', 'createtime')
    search_fields = (
        'electric__electricnumber',
        'electric__name',
        'device__deviceuuid',
        'device__name'
    )
    readonly_fields = ('registered', 'createtime')
    
    def electric_name(self, obj):
        return f"{obj.electric.name} ({obj.electric.electricnumber})"
    electric_name.short_description = 'Electric Number Name'
    
    def device_name(self, obj):
        return f"{obj.device.name} ({obj.device.deviceuuid})"
    device_name.short_description = 'Device Name'
    
    # 自定義表單中顯示的欄位
    fieldsets = (
        ('Binding Information', {
            'fields': (
                'electric',
                'device',
            )
        }),
        ('Status', {
            'fields': (
                'registered',
                'createtime',
            )
        }),
    )
    
    # 改善關聯對象的選擇介面
    autocomplete_fields = ['electric', 'device']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 優化下拉選單的顯示
        if db_field.name == "electric":
            kwargs["queryset"] = ElectricNumber.objects.filter(registered=True)
        if db_field.name == "device":
            kwargs["queryset"] = Device.objects.filter(registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
# @admin.register(ElectricNumber_Device_Band)
# class ElectricNumber_Device_Band_Admin(admin.ModelAdmin):
#     list_display = ['electric', 'device']
#     list_filter = ['electric']
#     search_fields = ['electric']

# Register your models here.

# @admin.register(Token)
# class CustomTokenAdmin(TokenAdmin):
#     list_display = ('key', 'user', 'created')
#     fields = ('user',)
#     ordering = ('-created',)