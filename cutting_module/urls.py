from django.urls import path
from . import views

urlpatterns = [

    #Fabric Summary API
    path('get_fabric_summary/', views.get_fabric_summary, name='get_fabric_summary'),
    path('get_fabric_summary/<str:jobno>/', views.get_fabric_summary, name='fabric_ocr_job'),
    path('get_fabric_ocr/', views.get_fabric_ocr, name='get_fabric_ocr'),
    path('fabric_inward_summary/', views.get_fabric_inward_summary, name='fabric_inward_summary'),
    path('fabric_delivery_summary/', views.get_fabric_delivery_summary, name='fabric_delivery_summary'),
    path('fabric_return_summary/', views.get_Fabric_return_summary, name='fabric_return_summary'),

    #Cutting Summary API
    path('get_cutting_summary/', views.get_cutting_summary, name='cutting_ocr'),
    path('get_cutting_summary/<str:jobno>/', views.get_cutting_summary, name='cutting_ocr_job_colour'),
    path('get_cutting_ocr/', views.get_cutting_ocr, name='get_cutting_ocr'),
    path('cutting_received/', views.get_fabric_received, name='cutting_received_summary'),
    path('cutting_consumption/', views.get_cutting_consumption, name='cutting_consumption_summary'),
    path('cutting_return/', views.get_cutting_return, name='cutting_return'),
    path('replace_details/', views.get_replace_details, name='replace_details'),
    path('cutting_stock_roll/', views.get_cutting_stock_roll, name='cutting_stock_roll'),
]