from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cutting_del_print/', views.cutting_del_print, name='cutting_del_print'),
    path('cutting_del_print/<int:id>/', views.cutting_del_print, name='cutting_del_print'),
]