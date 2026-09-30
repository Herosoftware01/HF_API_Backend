from django.urls import path
from . import views

urlpatterns = [
    
    # Operation Category Endpoints
    path('process_mas/', views.Process_Master, name='Process Master'),
    path('operations/', views.Operation_Category, name='Operation Master'),

]