from django.urls import path
from .views import *
from .import views
from django.conf.urls.static import static
from django.conf import settings

from .import views

urlpatterns = [
   
    path("qr_api", views.qr_api),
    path("emp_stick", views.emp_stick),
    path('save_checking/', views.save_checking),
    path('saved_plans/', views.get_saved_plans),
    path('final_bit_checking', views.bitchecking_final_data),
    path('check_final_saved', views.check_final_saved),
    path('delete_checking/',views.delete_checking,name='delete_checking'),
    path('delete_single_checking/',views.delete_single_checking,name='delete_single_checking'),
  
  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STAFF_IMAGES_URL, document_root=settings.STAFF_IMAGES_ROOT)
