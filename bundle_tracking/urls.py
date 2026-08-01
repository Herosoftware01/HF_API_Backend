from django.urls import path
from . import views

urlpatterns = [
    path('bundle_home/', views.bundle_home, name='bundle_home'),
    path('unit_login_api/', views.unit_login_api, name='unit_login_api'),
    path('allocate_unit/', views.allocate_unit, name='allocate_unit_query'),
    path('allocate_unit/<str:unitname>/', views.allocate_unit, name='allocate_unit'),
    path('approve_bundle/', views.approve_bundle, name='approve_bundle'),
    path("sub_bundle_report/<str:unit_id>/", views.sub_bundle_report, name="sub_bundle_report"),
    path("bundle_details/", views.fetch_bundle_details, name="fetch_bundle_details"),
    path("bundle_scan_update/", views.update_child_bundle_scan, name="bundle_scan_update"),
]
