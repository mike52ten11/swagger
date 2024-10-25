from rest_framework.permissions import BasePermission, SAFE_METHODS
from .serializers import UserInfoSerializer

class IsAdminOrAllowedEndpoint(BasePermission):
    allowed_endpoints = ['register','electricnumberregisterdevice','getamidata','userinfo', 'subscribestatus', 'changeuser']

    def has_permission(self, request, view):
        # 管理員可以訪問所有 API
        print(request.user)
        if request.user.is_staff:
            return True
        
        # 檢查視圖名稱是否在允許的端點列表中
        view_name = view.__class__.__name__.lower().replace('view', '')
        print(view_name)

        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data['account']
            print(account)
            return (view_name in self.allowed_endpoints) and (account==str(request.user))

        else:        
            return False