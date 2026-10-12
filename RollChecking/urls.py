from django.urls import path
from . import views

urlpatterns = [

    path('employees/', views.Roll_Employee, name='Roll_Employee'),
    path('emp-allocate/', views.Roll_Employee_Details, name='RollEmployeeDetails'),
    path('roll-list/', views.Roll_Checking, name='RollChecking'),
    path('checking-details/', views.RollChecking_Details, name='RollCheckingDetails'),
    path('checking-image-upload/', views.RollChecking_ImageUpload, name='RollCheckingImageUpload'),
    path('master-mistakes/', views.MasterMistakesList, name='MasterMistakesList')

]