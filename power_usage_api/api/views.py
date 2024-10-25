from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (   PowerUser, 
                        DeviceData,
                        DeviceElectricNumberMapping
                    )
from .serializers import (  PowerUserSerializer,
                            UserInfoSerializer,
                            ChangeUserSerializer,
                            SubscribeStatusSerializer,
                            DeleteUserSerializer,
                            DeviceDataSerializer,
                            GetDataSerializer,
                            DeviceUserMappingSerializer
                        )
from .permissions import IsAdminOrAllowedEndpoint                        


class RegisterView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        operation_summary="註冊/取消用戶服務",
        operation_description="""
        用於註冊新用戶或取消現有用戶的服務。
        
        參數說明：
        - electricnumber: 電號
        - account: 用戶帳號
        - registered: 註冊狀態（true/false）
        - regdate: 註冊日期
        
        回傳說明：
        - registerstatus: "1" 表示成功，"0" 表示失敗
        - reason: 失敗原因（如果失敗）
        """, 
        responses={
            200: openapi.Response(
                description="成功註冊/取消服務",
                examples={
                    "application/json": {
                        "registerstatus": "1"
                    }
                }
            ),
            400: openapi.Response(
                description="註冊/取消失敗",
                examples={
                    "application/json": {
                        "registerstatus": "0",
                        "reason": "重複啟用/重複取消/無效的數據"
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
            )
        ]
    )
    # @swagger_auto_schema(request_body=PowerUserSerializer)
    def post(self, request):
        serializer = PowerUserSerializer(data=request.data)
        if serializer.is_valid():

            electricnumber = serializer.validated_data['electricnumber']
            account = serializer.validated_data['account']
            registered = serializer.validated_data['registered']
            regdate = serializer.validated_data['regdate']

            user, created = PowerUser.objects.get_or_create(
                electricnumber=electricnumber,
                account=account
            )

            if user.registered == registered:
                # 重複操作的情況
                if registered:
                    reason = "重複啟用"
                else:
                    reason = "重複取消"
                return Response({
                    "registerstatus": "0",
                    "reason": reason
                }, status=status.HTTP_400_BAD_REQUEST)

            # 更新用戶狀態
            user.registered = registered
            user.regdate = regdate if registered else None
            user.save()
            
            return Response({
                "registerstatus": "1"
            }, status=status.HTTP_200_OK)
        
        return Response({
            "registerstatus": "0",
            "reason": "無效的數據"
        }, status=status.HTTP_400_BAD_REQUEST)


class ElectricnumberRegisterDeviceView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        operation_summary="電號綁定裝置",
        operation_description="""
        用於綁定電號和電表的uuid。
        
        參數說明：
        - electricnumber: 電號
        - deviceuuid: 電表的uuid
        - registered: 註冊狀態（true/false）
        - createtime: 綁定日期
        
        回傳說明：
        - registerstatus: "1" 表示成功，"0" 表示失敗
        - reason: 失敗原因（如果失敗）
        """, 
        responses={
            200: openapi.Response(
                description="成功綁定/取消綁定",
                examples={
                    "application/json": {
                        "registerstatus": "1"
                    }
                }
            ),
            400: openapi.Response(
                description="綁定失敗",
                examples={
                    "application/json": {
                        "registerstatus": "0",
                        "reason": "重複綁定/重複取消/無效的數據"
                    }
                }
            )
        },           
        request_body=DeviceUserMappingSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            )
        ]

    )   
    def post(self, request):
        serializer = DeviceUserMappingSerializer(data=request.data)
        if serializer.is_valid():

            electricnumber = serializer.validated_data['electricnumber']
            deviceuuid = serializer.validated_data['deviceuuid']
            registered = serializer.validated_data['registered']
            createtime = serializer.validated_data['createtime']

            user, created = DeviceElectricNumberMapping.objects.get_or_create(
                electricnumber=electricnumber,
                deviceuuid=deviceuuid
            )

            if user.registered == registered:
                # 重複操作的情況
                if registered:
                    reason = "重複啟用"
                else:
                    reason = "重複取消"
                return Response({
                    "registerstatus": "0",
                    "reason": reason
                }, status=status.HTTP_400_BAD_REQUEST)

            # 更新用戶狀態
            user.registered = registered
            user.createtime = createtime if registered else None
            user.save()
            
            return Response({
                "registerstatus": "1"
            }, status=status.HTTP_200_OK)
        
        return Response({
            "registerstatus": "0",
            "reason": "無效的數據"
        }, status=status.HTTP_400_BAD_REQUEST)



class UserInfoView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        operation_summary="查詢用戶資訊",
        operation_description="""
        根據用戶帳號查詢對應的電號資訊。
        
        參數說明：
        - account: 用戶帳號
        
        回傳說明：
        - account: 查詢的用戶帳號
        - electricnumber: 對應的電號列表
        """,
        request_body=UserInfoSerializer,
        responses={
            200: openapi.Response(
                description="成功查詢到用戶資訊",
                examples={
                    "application/json": {
                        "account": "0900123456",
                        "electricnumber": ["電號1", "電號2","..."]
                    }
                }
            ),
            404: openapi.Response(
                description="找不到用戶",
                examples={
                    "application/json": {
                        "account": "0900123456",
                        "electricnumber": []
                    }
                }
            ),
            400: 'Invalid data'       
        },        
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            )
        ]
    )  
    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data['account']


            condtions = {'account': account,
                    }            
            try:
                # user = PowerUserSerializer(condtions, many=True)
                users = PowerUser.objects.filter(account=account)
                if users.exists():
                    # 返回所有符合條件的電號列表
                    electric_numbers = [user.electricnumber for user in users]
                    return Response({
                        "account": account,
                        "electricnumber": electric_numbers
                    }, status=status.HTTP_200_OK)                
                
                else:
                    return Response({
                        "account": account,
                        "electricnumber": []
                    }, status=status.HTTP_404_NOT_FOUND)       

            
            except PowerUser.DoesNotExist:
                return Response({
                    "account": account,
                    "electricnumber": []
                }, status=status.HTTP_404_NOT_FOUND)


        return Response({
            "servicestatus": "0",
            "reason": "無效的數據"
        }, status=status.HTTP_400_BAD_REQUEST)


class SubscribeStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        operation_summary="查詢訂閱狀態",
        operation_description="""
        查詢指定電號和帳號的訂閱狀態。
        
        參數說明：
        - electricnumber: 電號
        - account: 用戶帳號
        
        回傳說明：
        - servicestatus: "1" 表示服務正常，"0" 表示服務異常
        - subscribestatus: "1" 表示已訂閱，"0" 表示未訂閱
        """,
        responses={
            200: openapi.Response(
                description="成功查詢訂閱狀態",
                examples={
                    "application/json": {
                        "servicestatus": "1",
                        "electricnumber": "電號",
                        "account": "帳號",
                        "subscribestatus": "1"
                    }
                }
            ),
            404: openapi.Response(
                description="查詢失敗",
                examples={
                    "application/json": {
                        "servicestatus": "0",
                        "reason": "請確認電號正確性(該用戶不存在於用戶清單內)"
                    }
                }
            ),
            400: 'Invalid data'
        },        
        request_body=SubscribeStatusSerializer,

        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="填入token", 
                type=openapi.TYPE_STRING
            )
        ]
    )        

    def post(self, request):
        serializer = SubscribeStatusSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = PowerUser.objects.get(
                    electricnumber=serializer.validated_data['electricnumber'],
                    account=serializer.validated_data['account']
                )
                return Response({
                    "servicestatus":"1",
                    "electricnumber": user.electricnumber,
                    "account": user.account,
                    "subscribestatus": "1" if user.registered else "0"
                }, status=status.HTTP_200_OK)
            except PowerUser.DoesNotExist:
                return Response({
                    "servicestatus":"0",
                    "reason": "請確認電號正確性(該用戶不存在於用戶清單內)"
                    
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "subscribestatus": "0"
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        request_body=ChangeUserSerializer,
        operation_summary="變更用戶帳號",
        operation_description="""
        變更用戶的帳號資訊。
        
        參數說明：
        - account: 原帳號
        - newaccount: 新帳號
        
        回傳說明：
        - changeuserstatus: "1" 表示變更成功，"0" 表示變更失敗
        """,
        responses={
            200: openapi.Response(
                description="成功變更帳號",
                examples={
                    "application/json": {
                        "changeuserstatus": "1"
                    }
                }
            ),
            404: openapi.Response(
                description="變更失敗",
                examples={
                    "application/json": {
                        "changeuserstatus": "0",
                        "reason": "User not found"
                    }
                }
            ),
            400: 'Invalid data'
        },        

        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            )
        ]
    )       

    def post(self, request):
        serializer = ChangeUserSerializer(data=request.data)
        if serializer.is_valid():
            old_account = serializer.validated_data['account']
            new_account = serializer.validated_data['newaccount']
            try:
                user = PowerUser.objects.get(account=old_account)
                user.account = new_account
                user.save()
                return Response({
                    "changeuserstatus": "1"
                }, status=status.HTTP_200_OK)
            except PowerUser.DoesNotExist:
                return Response({
                    "changeuserstatus": "0",
                    "reason": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "changeuserstatus": "0",
            "reason": "Invalid data"
        }, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        operation_summary="刪除用戶",
        operation_description="""
        刪除指定帳號的用戶資料。
        
        參數說明：
        - account: 要刪除的用戶帳號
        
        回傳說明：
        - deluserstatus: "1" 表示刪除成功，"0" 表示刪除失敗
        """,
        request_body=DeleteUserSerializer,
        responses={
            200: openapi.Response(
                description="成功刪除用戶",
                examples={
                    "application/json": {
                        "deluserstatus": "1"
                    }
                }
            ),
            404: openapi.Response(
                description="刪除失敗",
                examples={
                    "application/json": {
                        "deluserstatus": "0",
                        "reason": "User not found"
                    }
                }
            )
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            )
        ]
    )
    
    def post(self, request):
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data['account']

            try:
                user = PowerUser.objects.get(account=account)
                user.delete()
                return Response({
                    "deluserstatus": "1"
                }, status=status.HTTP_200_OK)
            except PowerUser.DoesNotExist:
                return Response({
                    "deluserstatus": "0",
                    "reason": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "deluserstatus": "0",
            "reason": "Invalid data"
        }, status=status.HTTP_400_BAD_REQUEST)


class DeviceDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]    
    @swagger_auto_schema(
        operation_summary="新增設備數據",
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
                schema=DeviceDataSerializer
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
        request_body=DeviceDataSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('deviceuuid', openapi.IN_QUERY, description="Device UUID", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Device name", type=openapi.TYPE_STRING),            
        ]
    )       
    # permission_classes = [IsAuthenticated]    

    def post(self, request):
    
        serializer = DeviceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAmiDataView(APIView):
    permission_classes = [IsAdminOrAllowedEndpoint]
    print(permission_classes)
    @swagger_auto_schema(
        operation_summary="查詢 AMI 數據",
        operation_description="""
        查詢特定設備在指定時間的 AMI 數據。
        
        參數說明：
        - deviceuuid: 設備唯一識別碼
        - name: 設備名稱
        - datatime: 查詢時間（Unix timestamp）
        
        回傳所有符合條件的數據記錄
        """,
        request_body=GetDataSerializer,
        responses={
            201: openapi.Response(
                description="成功查詢數據",
                schema=DeviceDataSerializer(many=True)
            ),
            400: openapi.Response(
                description="查詢失敗",
                examples={
                    "application/json": {
                        "error": "Invalid parameters"
                    }
                }
            )
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入token", 
                type=openapi.TYPE_STRING
            ),
            # openapi.Parameter('deviceuuid', openapi.IN_QUERY, description="Device UUID", type=openapi.TYPE_STRING),
            # openapi.Parameter('name', openapi.IN_QUERY, description="Device name", type=openapi.TYPE_STRING),            
        ]
    )       

    def post(self, request):
        
        serializer = GetDataSerializer(data=request.data)
        if serializer.is_valid():
            electricnumber = serializer.validated_data['electricnumber']
            try:
                mappingdata = DeviceElectricNumberMapping.objects.get(electricnumber=electricnumber)
            except:
                return Response('電號沒有對應的電錶', status=status.HTTP_404_NOT_FOUND)

            if mappingdata.registered:
                deviceuuid = mappingdata.deviceuuid
            else:
                return Response('電號對應的電錶尚未啟用', status=status.HTTP_404_NOT_FOUND)
            start = serializer.validated_data['start'] 

            
            queryset = DeviceData.objects.all()
            condtions = {'datatime': int(start),
                        'deviceuuid': deviceuuid,
                        }
            queryset = queryset.filter(**condtions)
            # if datatime:
            #     queryset = queryset.filter(datatime=datatime)
            # if deviceuuid:
            #     queryset = queryset.filter(deviceuuid=deviceuuid)
            # if name:
            #     queryset = queryset.filter(name=name)
            serializer = DeviceDataSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrAllowedEndpoint]
    @swagger_auto_schema(
        operation_summary="查詢 使用者 token(限管理者)",
        operation_description="""
        查詢特定設備在指定時間的 AMI 數據。
        
        參數說明：
        - username: 查詢Token的帳號
        回傳這個帳號的token
        """,
        responses={
            201: openapi.Response(
                description="成功查詢數據",
                schema=DeviceDataSerializer(many=True)
            ),
            404: openapi.Response(
                description="查詢失敗",
                examples={
                    "application/json": {
                        "error": "Invalid parameters"
                    }
                }
            )
        },            
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER, 
                description="輸入管理者token", 
                type=openapi.TYPE_STRING
            )
        ]
    )    
    
    def post(self, request, *args, **kwargs):

        User = get_user_model()
        username = request.data.get('username')
        # 查找目標用戶
        try:
            user = User.objects.get(username=username)
        except:
            return Response({
                "deluserstatus": "0",
                "reason": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)                   
        # 獲取或創建用戶的token
        token, created = Token.objects.get_or_create(user=user)


        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'account': user.email
        })                                            
        # if serializer.is_valid():                                
            # serializer = self.serializer_class(data=request.data,
            #                             context={'request': request})
        #     user = serializer.validated_data['user']
            
        #     token, created = Token.objects.get_or_create(user=user)
        #     return Response({
        #         'token': token.key,
        #         'user_id': user.pk,
        #         'email': user.email,
        #         'account': user.email
        #     })       
        # else:
            
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                            