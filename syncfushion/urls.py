from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GridSettingViewSet,token_api,reports_list_api, export_report_api

router = DefaultRouter()
router.register(r'grid-settings', GridSettingViewSet, basename='grid-settings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', token_api),
    path('reports/', reports_list_api),
    path("export/", export_report_api),
]
