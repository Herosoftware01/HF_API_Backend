from django.urls import path
from . import views

urlpatterns = [
    
    path('live_scan_data/', views.live_scan_data, name='live_scan_data'),
]  