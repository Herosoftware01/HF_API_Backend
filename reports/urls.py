from django.urls import path
from . import views

urlpatterns = [
    
    path('report/', views.holdwage_report, name='holdwage_report'),
    path('empwisesal/', views.empwisesal, name='empwisesal'),
    path("holdwagepaid/", views.holdwagepaid_api, name="holdwagepaid_api"),
    path('get_lay_sp_data/', views.get_lay_sp_data, name='get_lay_sp_data'),
    path('get_master_final_mistake_data/', views.get_master_final_mistake_data, name='get_master_final_mistake_data'),
    path('get_unit_bundle_data/', views.get_unit_bundle_report_data, name='get_unit_bundle_data'),
    path('mistake_summary/', views.mistake_summary, name='mistake_summary'),
    path('coraroll/', views.cora, name='coraroll'),
    path('attendance/', views.attendance, name='attendance'),
    path('absent_details/', views.abs_details, name='absent_details'),
    path('present_details/', views.present_details, name='present_details'),
    path('cutdel/', views.cutdel, name='cutdel'),

    ] 