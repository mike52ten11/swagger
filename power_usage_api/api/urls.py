from django.urls import path
from .views import (    RegisterView,
                        SubscribeStatusView, 
                        ChangeUserView, 
                        DeleteUserView,
                        DeviceDataView,
                        CustomObtainAuthToken,
                        GetAmiDataView,
                        UserInfoView,
                        ElectricnumberRegisterDeviceView
                    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register_electricnumber_to_device/', ElectricnumberRegisterDeviceView.as_view(), name='electricnumber-device'),

    # path('lifestyleservice/', LifestyleServiceView.as_view(), name='lifestyle-service'),
    path('subscribestatus/', SubscribeStatusView.as_view(), name='subscribe-status'),
    path('changeuser/', ChangeUserView.as_view(), name='change-user'),
    path('deluser/', DeleteUserView.as_view(), name='delete-user'),

    path('devicedata/', DeviceDataView.as_view(), name='device-data'),
    path('getamidata/', GetAmiDataView.as_view(), name='ami-data'),

    path('userinfo/', UserInfoView.as_view(), name='user-info'),

    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),


]