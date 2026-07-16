from django.urls import path
from . import views
from .views import UnitInputAPIView,GetUnitDataAPIView

urlpatterns = [
    
    path('live_scan_data/', views.live_scan_data, name='live_scan_data'),
    path('save-bundles/', UnitInputAPIView.as_view(), name='save-bundles'),
    path('get_input_scan_bundles/', GetUnitDataAPIView.as_view(), name='get_input_scan_bundles'),
]  