from django.urls import path
from . import views
from .views import UnitInputAPIView,GetUnitDataAPIView,GetUnitAssemply

urlpatterns = [
    
    path('live_scan_data/', views.live_scan_data, name='live_scan_data'),
    path('assembly_emp/', views.assembly_emp, name='assembly_emp'),
    path('save-assembly/', views.save_assembly, name='save-assembly'),
    path('save-bundles/', UnitInputAPIView.as_view(), name='save-bundles'),
    path('get_input_scan_bundles/', GetUnitDataAPIView.as_view(), name='get_input_scan_bundles'),
    path('get_assembly_bundles/', GetUnitAssemply.as_view(), name='get_assembly_bundles'),
]  
