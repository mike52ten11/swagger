

from rest_framework import serializers
from ..models import Device

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['deviceuuid', 'name', 'createtime','registered']    

class Device_Update_Serializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    registered = serializers.BooleanField(required=False)
    class Meta:
        model = Device
        fields = ['deviceuuid', 'name', 'registered']
        extra_kwargs = {
            'deviceuuid': {
                'validators': []  # 移除 UniqueValidator 用於更新操作
            },
            'name': {                
                'validators': []  # 移除 name 的唯一性驗證
            },
              
        }
                