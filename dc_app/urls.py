from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cutting_del_print/', views.cutting_del_print, name='cutting_del_print'),
    path('cutting_del_print/<int:id>/', views.cutting_del_print, name='cutting_del_print'),
    path('cutting_bit_print/<int:id>/', views.cutting_bit_print, name='CuttingBitPrint'),
    path('yarn_process_del/<int:dcno>/', views.yarn_process_delivery, name='YarnProcessDelivery'),
    path('knitting_del_print/', views.knitting_del_print, name='knitting_del_print'),
    path('knitting_del_print/<int:id>/', views.knitting_del_print, name='knitting_del_print'),
    path('acc_prod_del_print/', views.acc_prod_del_print, name='acc_prod_del_print'),
    path('acc_prod_del_print/<int:id>/', views.acc_prod_del_print, name='acc_prod_del_print'),
    path('acc_proc_del_print/', views.acc_proc_del_print, name='acc_proc_del_print'),
    path('acc_proc_del_print/<int:id>/', views.acc_proc_del_print, name='acc_proc_del_print'),
    path('acc_inward_verification/', views.acc_inward_verification, name='acc_inward_verification'),
    path('fabric_process_delivery/', views.fabric_process_delivery, name='FabricProcessDelivery'),
    path('fabric_process_delivery/<int:dcno>/', views.fabric_process_delivery, name='FabricProcessDelivery'),
    path('mistake_qty_print/', views.mistake_qty_print, name='mistake_qty_print'),
    path('mistake_qty_print/<int:id>/', views.mistake_qty_print, name='mistake_qty_print'),
    
]