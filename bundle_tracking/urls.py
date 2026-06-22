from django.urls import path
from . import views

urlpatterns = [
    path('bundle_home/', views.bundle_home, name='bundle_home'),
    path('unit_login_api/', views.unit_login_api, name='unit_login_api'),
    path('allocate_unit/<str:unitname>/', views.allocate_unit, name='allocate_unit'),
]