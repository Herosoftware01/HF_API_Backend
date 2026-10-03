from django.urls import path
from . import views

urlpatterns = [
    
    # Operation Category Endpoints
    path('process_mas/', views.Process_Master, name='Process Master'),
    path('emp_details/', views.Employee_Details, name='Employee Details'),
    path('operations/', views.Operation_Category, name='Operation Master'),
    path('approval/', views.Approval, name='Approval'),
    path('assessment/', views.Individual_Assessment, name='Assessment'),

]