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

        electricnumber = request.data.get('electricnumber')
        if not electricnumber:
            return Response({
                'status': '0',
                'reason': 'electricnumber is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            electric = ElectricNumber.objects.get(electricnumber=electricnumber)
        except ElectricNumber.DoesNotExist:
            return Response({
                'status': '0',
                'reason': 'electricnumber not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ElectricNumber_Update_Serializer(electric, data=request.data, partial=True)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response({
                'status': '1',
                'reason': 'Success'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': '0',
                'reason': f"Invalid data {serializer.errors}"
            }, status=status.HTTP_400_BAD_REQUEST)
