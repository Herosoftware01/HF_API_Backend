from django.urls import path
from . import views

urlpatterns = [
    path('ws_attendance/', views.ws_attendance, name='ws_attendance'),
]