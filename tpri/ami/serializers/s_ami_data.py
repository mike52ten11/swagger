from rest_framework import serializers
from ..models import AMIData, User_Banding_ElectricNumber, ElectricNumber_Device_Band, Device

class AMIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AMIData
        fields = ['deviceuuid', 'name', 'value', 'datatime']

    def create(self, validated_data):
        return AMIData.objects.create(**validated_data)

class GetAMIDataSerializer(serializers.Serializer):
    datatime = serializers.IntegerField()

    def validate(self, data):
        # 從 context 中獲取 user
        user = self.context['request'].user
        
        # 檢查用戶綁定的電號
        user_binding = User_Banding_ElectricNumber.objects.filter(
            user=user,
            registered=True
        ).first()
        
        if not user_binding:
            raise serializers.ValidationError("使用者未綁定電號或電號未啟用")

        # 檢查電號綁定的設備
        device_binding = ElectricNumber_Device_Band.objects.filter(
            electricnumber=user_binding.electricnumber,
            registered=True
        ).first()
        
        if not device_binding:
            raise serializers.ValidationError("device未啟用或device未綁定電號")
        

        # 將 deviceuuid 添加到驗證後的數據中
        data['deviceuuid'] = device_binding.device.deviceuuid
        return data




