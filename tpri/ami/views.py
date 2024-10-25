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

from .models import (   PowerUser, 
                        Device,
                    )
from .serializers.s_user import UserRegistrationSerializer, PowerUserSerializer
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

class PowerUserRegisterView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]    
    @swagger_auto_schema(
        operation_summary="用戶註冊",
        operation_description="""
        新增設備的測量數據。
        
        參數說明：
        - deviceuuid: 設備唯一識別碼
        - name: 設備名稱
        - value: 測量值
        - datatime: 數據時間
        - createtime: 建立時間
        
        所有時間都使用 Unix timestamp 格式
        """,
        responses={
            201: openapi.Response(
                description="成功新增數據",
                schema=PowerUserSerializer
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
        request_body=PowerUserSerializer,
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
        return PowerUserRegistrationView().post(request)

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
# class GetAmiDataView(APIView):
#     permission_classes = [IsAdminOrAllowedEndpoint]
#     print(permission_classes)
#     @swagger_auto_schema(
#         operation_summary="查詢 AMI 數據",
#         operation_description="""
#         查詢特定設備在指定時間的 AMI 數據。
        
#         參數說明：
#         - deviceuuid: 設備唯一識別碼
#         - name: 設備名稱
#         - datatime: 查詢時間（Unix timestamp）
        
#         回傳所有符合條件的數據記錄
#         """,
#         request_body=GetDataSerializer,
#         responses={
#             201: openapi.Response(
#                 description="成功查詢數據",
#                 schema=DeviceDataSerializer(many=True)
#             ),
#             400: openapi.Response(
#                 description="查詢失敗",
#                 examples={
#                     "application/json": {
#                         "error": "Invalid parameters"
#                     }
#                 }
#             )
#         },
#         manual_parameters=[
#             openapi.Parameter(
#                 'Authorization', 
#                 openapi.IN_HEADER, 
#                 description="輸入token", 
#                 type=openapi.TYPE_STRING
#             ),
#             # openapi.Parameter('deviceuuid', openapi.IN_QUERY, description="Device UUID", type=openapi.TYPE_STRING),
#             # openapi.Parameter('name', openapi.IN_QUERY, description="Device name", type=openapi.TYPE_STRING),            
#         ]
#     )       

#     def post(self, request):
        
#         serializer = GetDataSerializer(data=request.data)
#         if serializer.is_valid():
#             electricnumber = serializer.validated_data['electricnumber']
#             try:
#                 mappingdata = DeviceElectricNumberMapping.objects.get(electricnumber=electricnumber)
#             except:
#                 return Response('電號沒有對應的電錶', status=status.HTTP_404_NOT_FOUND)

#             if mappingdata.registered:
#                 deviceuuid = mappingdata.deviceuuid
#             else:
#                 return Response('電號對應的電錶尚未啟用', status=status.HTTP_404_NOT_FOUND)
#             start = serializer.validated_data['start'] 

            
#             queryset = DeviceData.objects.all()
#             condtions = {'datatime': int(start),
#                         'deviceuuid': deviceuuid,
#                         }
#             queryset = queryset.filter(**condtions)
#             # if datatime:
#             #     queryset = queryset.filter(datatime=datatime)
#             # if deviceuuid:
#             #     queryset = queryset.filter(deviceuuid=deviceuuid)
#             # if name:
#             #     queryset = queryset.filter(name=name)
#             serializer = DeviceDataSerializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)  
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomObtainAuthToken(APIView):
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAdminOrAllowedEndpoint]
#     @swagger_auto_schema(
#         operation_summary="查詢 使用者 token(限管理者)",
#         operation_description="""
#         查詢特定設備在指定時間的 AMI 數據。
        
#         參數說明：
#         - username: 查詢Token的帳號
#         回傳這個帳號的token
#         """,
#         responses={
#             201: openapi.Response(
#                 description="成功查詢數據",
#                 schema=DeviceDataSerializer(many=True)
#             ),
#             404: openapi.Response(
#                 description="查詢失敗",
#                 examples={
#                     "application/json": {
#                         "error": "Invalid parameters"
#                     }
#                 }
#             )
#         },            
#         manual_parameters=[
#             openapi.Parameter(
#                 'Authorization', 
#                 openapi.IN_HEADER, 
#                 description="輸入管理者token", 
#                 type=openapi.TYPE_STRING
#             )
#         ]
#     )    
    
#     def post(self, request, *args, **kwargs):

#         User = get_user_model()
#         username = request.data.get('username')
#         # 查找目標用戶
#         try:
#             user = User.objects.get(username=username)
#         except:
#             return Response({
#                 "deluserstatus": "0",
#                 "reason": "User not found"
#             }, status=status.HTTP_404_NOT_FOUND)                   
#         # 獲取或創建用戶的token
#         token, created = Token.objects.get_or_create(user=user)


#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email,
#             'account': user.email
#         })                                            
#         # if serializer.is_valid():                                
#             # serializer = self.serializer_class(data=request.data,
#             #                             context={'request': request})
#         #     user = serializer.validated_data['user']
            
#         #     token, created = Token.objects.get_or_create(user=user)
#         #     return Response({
#         #         'token': token.key,
#         #         'user_id': user.pk,
#         #         'email': user.email,
#         #         'account': user.email
#         #     })       
#         # else:
            
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                            