from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GridSettingViewSet,token_api,reports_list_api, export_report_api

from . import views

router = DefaultRouter()
router.register(r'grid-settings', GridSettingViewSet, basename='grid-settings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', token_api),
    path('reports/', reports_list_api),
    path("export/", export_report_api),

    path('mail/add/', views.add_mail, name='add_mail'),
    path('mail/get_mails/', views.get_mails, name='add_mail'),
    path('mail/update/<int:pk>/', views.update_mail, name='update_mail'),
    path('mail/delete/<int:pk>/', views.delete_mail, name='delete_mail'),
]
