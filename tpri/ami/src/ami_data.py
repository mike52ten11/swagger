from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import AMIData
from ..serializers.s_ami_data import AMIDataSerializer, GetAMIDataSerializer

class MyAMIDataView(APIView):    


    def create(self, request):
        serializer = AMIDataSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        deviceuuid = request.data.get('deviceuuid')
        datatime = request.data.get('datatime')
        
        try:
            instance = AMIData.objects.get(deviceuuid=deviceuuid, datatime=datatime)
            instance.delete()
            
            return Response({"ststus": 1, 
                            "message":"刪除成功"
                            },status=status.HTTP_200_OK
                            )
        except AMIData.DoesNotExist:
            return Response({"ststus": 0, 
                            "message":"資料已不存在，刪除失敗"
                            },
                            status=status.HTTP_404_NOT_FOUND)
    

    @action(detail=False, methods=['patch'])
    def update_value(self, request):
        deviceuuid = request.data.get('deviceuuid')
        datatime = request.data.get('datatime')
        value = request.data.get('value')
        
        try:
            instance = AMIData.objects.get(deviceuuid=deviceuuid, datatime=datatime)
            instance.value = value
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except AMIData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def get_ami_data(self, request):
        serializer = GetAMIDataSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # 從驗證後的數據中獲取 deviceuuid 和 datatime
            deviceuuid = serializer.validated_data['deviceuuid']
            datatime = serializer.validated_data['datatime']
            print(deviceuuid)
            print(datatime)
         
            try:
                ami_data = AMIData.objects.get(deviceuuid=deviceuuid, datatime=datatime)
                return Response({
                    'value': ami_data.value
                })
            except AMIData.DoesNotExist:
                return Response(
                    {"error": "找不到對應的 AMI 數據"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            