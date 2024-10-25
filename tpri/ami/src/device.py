from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.s_device import DeviceSerializer
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
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():

            try:
                device = Device.objects.get(deviceuuid=serializer.validated_data['deviceuuid'])
                device.name = serializer.validated_data['name']
                device.save()   
                return Response({
                    "status": "1"
                }, status=status.HTTP_200_OK)
            except Device.DoesNotExist:
                return Response({
                    "status": "0",
                    "reason": "Deviceuuid not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "status": "0",
            "reason": "Invalid data"
        }, status=status.HTTP_400_BAD_REQUEST)