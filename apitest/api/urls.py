from django.contrib import admin
from django.urls import path
from api.swagger import schema_view
from api.views import SampleAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sample/', SampleAPIView.as_view(), name='sample_api'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
]