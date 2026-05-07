from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('request/', views.request_advance, name='request'),  
    path('eligibleamt/', views.get_eligibleamt, name='get_eligibleamt'),
    path('empwisesal/', views.empwisesal, name='empwisesal'),
    path('ad_approve/', views.ad_approve, name='ad_approve'),
    path('state/', views.state, name='state'),
    path('send-advance-mail/', views.send_advance_mail, name='send_advance_mail'),
    path('approve_mail/', views.send_approval_mail, name='approve_mail'),
<<<<<<< HEAD
    path('g_contact/', views.google_contact_api, name='g_contact'),
    path('new_pros/', views.new_pros, name='new_pros'),
=======

    path('fab_cut_report/', views.fabric_cutting, name='fabric_cutting'),
>>>>>>> 431ded575a06f6c598b95fbf5619786525777877
]   