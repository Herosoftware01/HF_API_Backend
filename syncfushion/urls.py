from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GridSettingViewSet

router = DefaultRouter()
router.register(r'grid-settings', GridSettingViewSet, basename='grid-settings')

urlpatterns = [
    path('api/', include(router.urls)),
]