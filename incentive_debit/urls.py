from django.urls import path
from . import views


urlpatterns = [
    path('api/staff/', views.staff_full_details, name='staff_full_details'),
    path('api/emp/', views.empwise_salary_api, name='empwise_salary_api'),
    
    # Main Transaction Logs
    path('api/incdeb/', views.incdeb_list_create, name='incdeb-list-create'),
    path('api/incdeb/<int:req_id>/', views.incdeb_update, name='incdeb-update'),
    path("api/incdeb-status/", views.incdeb_status_api, name='incdeb_status_api'),

    # Users Management
    path("api/incdeb_users/", views.incdeb_users_api, name='incdeb_users_api'),
    path("api/incdeb_users/<int:pk>/", views.incdeb_users_detail_api, name='incdeb_users_delete'), # <--- ADD THIS

    # Purpose Management
    path("api/incdeb_purpose/", views.incdeb_purpose_api, name='incdeb_purpose_api'),
    path("api/incdeb_purpose/<int:pk>/", views.incdeb_purpose_detail_api, name='incdeb_purpose_delete'), # <--- ADD THIS

]