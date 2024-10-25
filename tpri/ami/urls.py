from django.urls import path
from .views import (    UserRegistrationView,
                        PowerUserRegisterView,
                        DeviceRegistratioView,
                        ElectricNumberView,
                        TokenManagementView,
                        ElectricNumberDeviceBindingView
                    )

urlpatterns = [
    path('user-register/', UserRegistrationView.as_view(), name='user-register'),
    path('device-register/', DeviceRegistratioView.as_view(), name='device-register'),
    path('electricnumber-register/', ElectricNumberView.as_view(), name='electricnumber-register'),
    path('device-binding/', ElectricNumberDeviceBindingView.as_view(), name='device-binding'),
    path('token/', TokenManagementView.as_view(), name='token-management'),

]