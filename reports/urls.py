from django.urls import path
from . import views

urlpatterns = [
    

    path('get_lay_sp_data/', views.get_lay_sp_data, name='get_lay_sp_data'),
    path('get_master_final_mistake_data/', views.get_master_final_mistake_data, name='get_master_final_mistake_data'),
    path('get_unit_bundle_data/', views.get_unit_bundle_report_data, name='get_unit_bundle_data'),
    path('mistake_summary/', views.mistake_summary, name='mistake_summary'),
    path('coraroll/', views.cora, name='coraroll'),
    path('cutdel/', views.cutdel, name='cutdel'),
    path('bitcheckhour/', views.bitcheckhour, name='bitcheckhour'),
    path('stickerhour/', views.stickerHour, name='stickerHour'),
    path('measurement_report/', views.measurement_report, name='measurement_report'),

    # HR Reports
    path('empwisesal/', views.empwisesal, name='empwisesal'),
    
    # Finance Reports
    path('dyeing_data/', views.dyeing_data , name='dyeing_data'),
    path('dyeing_order_details/', views.dyeing_order_details , name='dyeing_order_details'),

    # Cutting Reports
    path('cutting_details/', views.GetCuttingDetails, name='get_cutting_details'),
    path('aprod_details/', views.GetAprodDetails, name='get_aprod_details'),
    path('repcut_pend/', views.RepcutPending, name='RepCutPending'),
    path('rep_cut_pend/', views.RepCutPending, name='RepCutPending'),
    path('cutting_replace_pending/', views.Cutting_Replace_Pending, name='Cutting_Replace_Pending'),
    path('master_repcut/', views.Master_Repcut, name='Master_Repcut'),
    path('master_repcut_details/', views.Master_Repcut_Details, name='Master_Repcut_Details'),

   
] 