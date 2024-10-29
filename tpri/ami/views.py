from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (   User_Banding_ElectricNumber, 
                        Device,
                    )
from .serializers.s_user import UserRegistrationSerializer
from .serializers.s_device import DeviceSerializer
from .serializers.s_electric_number import (    ElectricNumberSerializer, 
                                                ElectricNumber_Update_Serializer
                                            )
from .serializers.s_electricnumber_device_band import ElectricNumberDeviceBindingSerializer

from .permissions import IsAdminOrAllowedEndpoint  

from .src.user import (     MyUserRegistrationView,
                            MyTokenManagementView
                        )

from .src.device import (     MyDevice
                        )

from .src.electric_number import    (     MyElectricNumber

                                    )        
from .src.electricnumber_device_band import    (     MyElectricNumberDeviceBindingView

                                                 )     
                                          
from .src.user_electricnumber_band import    (     MyUserElectricNumberBindingView

                                                 )     
from .src.ami_data import    (     MyAMIDataView

                                                 )   
                                                 
                                                                                                     
'''
 一般使用者的api
 1. 註冊
 2. 查token
 3. 使用者-電號 綁定

'''
class UserRegistrationView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    def post(self, request):

        return MyUserRegistrationView().post(request)
class TokenManagementView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    def post(self, request):

        return MyTokenManagementView().post(request)
'''
 管理者api

 一、使用者管理
    1. 使用者 刪除/停用/啟用
    2. token 查詢/刪除

 二、裝置管理 
    1. 電表uuid 新增/刪除

 三、電號管理
    1. 電號 新增/刪除

 四、 綁定 電號-裝置uuid 管理
    1. 電號-裝置uuid 綁定

'''

class DeviceRegistratioView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]    
    @swagger_auto_schema(
        operation_summary="新增設備數據",
        operation_description="""
        新增設備的測量數據。
        
        參數說明：
        - deviceuuid: 設備唯一識別碼
        - name: 設備名稱
        - createtime: 建立時間
        
        所有時間都使用 Unix timestamp 格式
        """,
        responses={
            201: openapi.Response(
                description="成功新增數據",
                schema=DeviceSerializer
            ),
            400: openapi.Response(
                description="新增失敗",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            )
        },        
        request_body=DeviceSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            ),         
        ]
    )       

    def post(self, request):
    
        return MyDevice().post(request)

    def patch(self, request):
    
        return MyDevice().patch(request)


class ElectricNumberView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]    
    @swagger_auto_schema(
        operation_summary="新增電號(僅限管理者)",
        operation_description="""
        新增設備的測量數據。
        
        參數說明：
            - electric number: 電號唯一識別碼
            - name: 電號名稱
        
        所有時間都使用 Unix timestamp 格式
        """,
        responses={
            201: openapi.Response(
                description="成功新增數據",
                schema=ElectricNumberSerializer
            ),
            400: openapi.Response(
                description="新增失敗",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            )
        },        
        request_body=ElectricNumberSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            ),         
        ]
    )       

    def post(self, request):
    
        return MyElectricNumber().post(request)

    @swagger_auto_schema(
        operation_summary="修改電號名稱",
        operation_description="""
        修改電號名稱。
        
        參數說明：
        - electric number: 電號唯一識別碼
        - name: 電號名稱
        
        """,
        responses={
            201: openapi.Response(
                description="成功修改數據",
                schema=ElectricNumber_Update_Serializer
            ),
            400: openapi.Response(
                description="修改失敗",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            )
        },        
        request_body=ElectricNumber_Update_Serializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            ),         
        ]
    )       
    def patch(self, request):
    
        return MyElectricNumber().patch(request)

class ElectricNumberDeviceBindingView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    def post(self, request):
        return MyElectricNumberDeviceBindingView().post(request)
    def delete(self, request):
        return MyElectricNumberDeviceBindingView().delete(request)
    def get(self, request):  
        return MyElectricNumberDeviceBindingView().get(request)  


class UserElectricNumberBindingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrAllowedEndpoint]
    def post(self, request):
        return MyUserElectricNumberBindingView().post(request)
    def delete(self, request):
        return MyUserElectricNumberBindingView().delete(request)
    def get(self, request):  
        return MyUserElectricNumberBindingView().get(request)          


class AMIDataView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrAllowedEndpoint]
    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "只有管理員可以刪除數據"}, 
                status=status.HTTP_403_FORBIDDEN
            )           
        return MyAMIDataView().create(request)

    def delete(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "只有管理員可以刪除數據"}, 
                status=status.HTTP_403_FORBIDDEN
            )        
        return MyAMIDataView().delete(request)

    def patch(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "只有管理員可以刪除數據"}, 
                status=status.HTTP_403_FORBIDDEN
            )           
        return MyAMIDataView().patch(request)

    def get(self, request):  
        
        return MyAMIDataView().get_ami_data(request)  