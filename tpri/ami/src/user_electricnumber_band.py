from django.db import transaction
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User_Banding_ElectricNumber
from ..serializers.s_user_electricnumber_band import UserElectricNumberBindingSerializer

class MyUserElectricNumberBindingView(APIView):
    def post(self, request):
        serializer = UserElectricNumberBindingSerializer(data=request.data)
        
        if serializer.is_valid():
            # 檢查是否已存在相同的綁定
            existing_binding = User_Banding_ElectricNumber.objects.filter(
                user=request.user,
                electricnumber=serializer.validated_data['electricnumber']
            ).first()
            
            if existing_binding:
                return Response({
                    "message": "Binding already exists",
                    # "data": {
                    #     "account": existing_binding.account,
                    #     "electricnumber": existing_binding.electricnumber.electricnumber,
                    #     "registered": existing_binding.registered,
                    #     "regdate": existing_binding.regdate
                    # }
                }, status=status.HTTP_400_BAD_REQUEST)            
            try:
                with transaction.atomic():
                    # 創建綁定記錄
                    binding = User_Banding_ElectricNumber(
                        user=request.user,
                        electricnumber=serializer.validated_data['electricnumber']
                    )
                    binding.clean()  # 執行驗證
                    binding.save()
                    
                    return Response({
                        "message": "Binding successful",
                        "data": {
                            "account": binding.account,
                            "electricnumber": binding.electricnumber.electricnumber,
                            "registered": binding.registered,
                            "regdate": binding.regdate
                        }
                    }, status=status.HTTP_201_CREATED)
                    
            except ValidationError as e:
                return Response({
                    "message": "Binding failed",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # 獲取當前用戶的所有綁定
        bindings = User_Banding_ElectricNumber.objects.filter(user=request.user)
        data = [{
            "account": binding.account,
            "electricnumber": binding.electricnumber.electricnumber,
            "registered": binding.registered,
            "regdate": binding.regdate
        } for binding in bindings]
        
        return Response(data)

    def delete(self, request):
        electricnumber = request.data.get('electricnumber')
        
        try:
            binding = User_Banding_ElectricNumber.objects.get(
                user=request.user,
                electricnumber__electricnumber=electricnumber
            )
            binding.delete()
            
            return Response({
                "message": "Unbinding successful"
            }, status=status.HTTP_200_OK)
            
        except User_Banding_ElectricNumber.DoesNotExist:
            return Response({
                "message": "Binding not found"
            }, status=status.HTTP_404_NOT_FOUND)