from rest_framework import serializers
from ..models import ElectricNumber_Device_Band, ElectricNumber, Device

class ElectricNumberDeviceBindingSerializer(serializers.Serializer):
    electricnumber = serializers.CharField(max_length=11)
    deviceuuid = serializers.CharField(max_length=36)

    def validate(self, data):
        # 驗證 electricnumber 是否存在
        try:
            electric = ElectricNumber.objects.get(electricnumber=data['electricnumber'])
        except ElectricNumber.DoesNotExist:
            raise serializers.ValidationError({"electricnumber": "ElectricNumber not found"})

        # 驗證 deviceuuid 是否存在
        try:
            device = Device.objects.get(deviceuuid=data['deviceuuid'])
        except Device.DoesNotExist:
            raise serializers.ValidationError({"deviceuuid": "Device not found"})

        # 檢查是否已經綁定
        if ElectricNumber_Device_Band.objects.filter(
            electric=electric,
            device=device
        ).exists():
            raise serializers.ValidationError("This binding already exists")

        # 將實例添加到驗證後的數據中
        data['electric'] = electric
        data['device'] = device
        return data

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class DeviceBindingView(APIView):
    def post(self, request):
        serializer = BindingSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # 創建綁定記錄
                    binding = ElectricNumber_Device_Band.objects.create(
                        electric=serializer.validated_data['electric'],
                        device=serializer.validated_data['device']
                    )
                    
                    return Response({
                        "message": "Binding successful",
                        "data": {
                            "electricnumber": binding.electric.electricnumber,
                            "deviceuuid": binding.device.deviceuuid,
                            "registered": binding.registered,
                            "createtime": binding.createtime
                        }
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    "message": "Binding failed",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = BindingSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                binding = ElectricNumber_Device_Band.objects.get(
                    electric=serializer.validated_data['electric'],
                    device=serializer.validated_data['device']
                )
                binding.delete()
                
                return Response({
                    "message": "Unbinding successful"
                }, status=status.HTTP_200_OK)
                
            except ElectricNumber_Device_Band.DoesNotExist:
                return Response({
                    "message": "Binding not found"
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        electricnumber = request.query_params.get('electricnumber')
        deviceuuid = request.query_params.get('deviceuuid')
        
        filters = {}
        if electricnumber:
            filters['electric__electricnumber'] = electricnumber
        if deviceuuid:
            filters['device__deviceuuid'] = deviceuuid
            
        bindings = ElectricNumber_Device_Band.objects.filter(**filters)
        
        data = [{
            "electricnumber": binding.electric.electricnumber,
            "deviceuuid": binding.device.deviceuuid,
            "registered": binding.registered,
            "createtime": binding.createtime
        } for binding in bindings]
        
        return Response(data)