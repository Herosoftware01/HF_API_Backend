from django.urls import path
from . import views

urlpatterns = [
    path('holdwage_report/', views.holdwage_report, name='holdwage_report'),
    path("holdwagepaid/", views.holdwagepaid_api, name="holdwagepaid_api"),
    path('bill_age/', views.bill, name='bill_age'),
    path('pass_age/', views.pass_data_api, name='pass_age'),
    path('bill_mdapprove/', views.approval_api, name='bill_mdapprove'),
    path('bill_dash/', views.bill_dashboard , name='bill_dash'),
    path('bill_details/', views.bill_details , name='bill_details'),
    path('pay_dash/', views.pay_dashboard , name='pay_dash'),
    path('pay_details/', views.pay_bill_details , name='pay_details'),

]