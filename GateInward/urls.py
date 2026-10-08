from django.urls import path
from . import views 

urlpatterns = [
    path('po_details/', views.po_details, name='po_details'),
    path('po_inward/', views.GatemoduleInward, name='GatemoduleInward'),
]