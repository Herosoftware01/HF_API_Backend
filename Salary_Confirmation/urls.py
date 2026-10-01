from django.urls import path
from . import views

urlpatterns = [
    # Machine Category Endpoints
    path('machines/', views.machine_category_api, name='machine-api'),
    path('machines/<int:id>/', views.machine_category_api, name='machine-api-detail'),
    
    # Operation Category Endpoints
    path('operations/', views.operation_category_api, name='operation-api'),
    path('operations/<int:id>/', views.operation_category_api, name='operation-api-detail'),
]