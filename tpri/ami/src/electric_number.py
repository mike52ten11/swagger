from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.s_electric_number import ElectricNumberSerializer,ElectricNumber_Update_Serializer
from django.core.exceptions import ObjectDoesNotExist

from ..models import ElectricNumber

class MyElectricNumber(APIView):

    def post(self, request):
        serializer = ElectricNumberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        
        serializer = ElectricNumber_Update_Serializer(data=request.data)
        
        if serializer.is_valid():

            try:
                electricnumber = ElectricNumber.objects.get(electricnumber=serializer.validated_data['electricnumber'])
                electricnumber.name = serializer.validated_data['name']
                electricnumber.save()   
                return Response({
                    "status": "1"
                }, status=status.HTTP_200_OK)

            except ElectricNumber.DoesNotExist:
                return Response({
                    "status": "0",
                    "reason": "electricnumber not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "status": "0",
            "reason": f"Invalid data {serializer.errors}"
        }, status=status.HTTP_400_BAD_REQUEST)