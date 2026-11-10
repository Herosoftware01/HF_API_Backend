from django.urls import path
from . import views

urlpatterns = [
    path('fabric_ocr/', views.get_fabric_summary, name='get_fabric_summary'),
    path('fabric_ocr/<str:jobno>/', views.get_fabric_summary, name='fabric_ocr_job'),
    path('fabric_inward_summary/', views.get_fabric_inward_summary, name='fabric_inward_summary'),
    path('fabric_delivery_summary/', views.get_fabric_delivery_summary, name='fabric_delivery_summary'),
    path('cutting_return_summary/', views.get_cutting_return_summary, name='cutting_return_summary'),
]