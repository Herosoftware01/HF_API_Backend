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
    path('cutdel/', views.cutdel, name='cutdel'),

    # HR Reports
    path('attendance/', views.attendance, name='attendance'),
    path('absent_details/', views.abs_details, name='absent_details'),
    path('present_details/', views.present_details, name='present_details'),
    path('resign_report/', views.resign_report, name='resign_report'),
    path('join_data/', views.join_data, name='join_data'),
    path('staff_overview/', views.staff_overview, name='staff_overview'),
    path('staff_pre/', views.staff_pre, name='staff_pre'),
    path('staff_abe/', views.staff_abe, name='staff_abe'),
    path('staff_one/', views.staff_report_api, name='staff_report_api'), 
    path('emp_one/', views.oneday_api, name='oneday_api'), 
    path('security_list/', views.security_list, name='security_list'),
    path('work_report/', views.workforce_trends_api, name='workforce_trends_api'),
    path('work_report1/', views.workforce_unit_trends_api, name='workforce_unit_trends_api'), 



    # Finance Reports
    path('bill_age/', views.bill, name='bill_age'),
    path('pass_age/', views.pass_data_api, name='pass_age'),
    path('bill_mdapprove/', views.approval_api, name='bill_mdapprove'),
    path('bill_dash/', views.bill_dashboard , name='bill_dash'),
    path('bill_details/', views.bill_details , name='bill_details'),
    path('pay_dash/', views.pay_dashboard , name='pay_dash'),
    path('pay_details/', views.pay_bill_details , name='pay_details'),

    ] 