from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.s_device import DeviceSerializer,Device_Update_Serializer
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

from ..models import Device

class MyDevice(APIView):

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        deviceuuid = request.data.get('deviceuuid')
        if not deviceuuid:
            return Response({
                'status': '1',
                'reason': 'deviceuuid is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(deviceuuid=deviceuuid)
        except Device.DoesNotExist:
            return Response({
                'status': '1',
                'reason': 'Device not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = Device_Update_Serializer(device, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': '1',
                'reason': 'Success'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': '1',
                'reason': f"Invalid data {serializer.errors}"
            }, status=status.HTTP_400_BAD_REQUEST)