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
]