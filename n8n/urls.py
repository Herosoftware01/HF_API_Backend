from django.urls import path
from . import views

urlpatterns = [
    path('ws_attandence/', views.ws_attandence, name='ws_attandence'),
]