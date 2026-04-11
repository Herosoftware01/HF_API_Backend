from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.holdwage_report, name='holdwage_report'),
    path('empwisesal/', views.empwisesal, name='empwisesal'),
    path("holdwagepaid/", views.holdwagepaid_api, name="holdwagepaid_api"),
    ] 