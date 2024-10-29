from django.urls import path
from .views import (    UserRegistrationView,
                        DeviceRegistratioView,
                        ElectricNumberView,
                        TokenManagementView,
                        ElectricNumberDeviceBindingView,
                        UserElectricNumberBindingView,
                        AMIDataView
                    )

urlpatterns = [
    path('user-register/', UserRegistrationView.as_view(), name='user-register'),
    path('device-register/', DeviceRegistratioView.as_view(), name='device-register'),
    path('electricnumber-register/', ElectricNumberView.as_view(), name='electricnumber-register'),
    path('device-binding/', ElectricNumberDeviceBindingView.as_view(), name='device-binding'),
    path('user-binding/', UserElectricNumberBindingView.as_view(), name='user-binding'),
    path('ami-data/', AMIDataView.as_view(), name='ami-data'),

    path('token/', TokenManagementView.as_view(), name='token-management'),

]