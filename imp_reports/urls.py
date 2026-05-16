from django.urls import path
from . import views

urlpatterns = [
    path('get_lay_sp_data/', views.get_lay_sp_data, name='get_lay_sp_data'),
    path('get_master_final_mistake_data/', views.get_master_final_mistake_data, name='get_master_final_mistake_data'),
    path('get_unit_bundle_data/', views.get_unit_bundle_report_data, name='get_unit_bundle_data'),
    path('mistake_summary/', views.mistake_summary, name='mistake_summary'),
    path('coraroll/', views.cora, name='coraroll'),
    path('unit_bundle/',views.unit_bundle,name='unit_bundle'),
    path('lay_sal/',views.lay_sp_sal,name='lay_sal'),
    path('qc_first/', views.qcfirst, name='qc_first'),
    path('qc_roving/', views.qcroving, name='qc_roving'),
]  