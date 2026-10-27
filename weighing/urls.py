from django.urls import path
from .views import scale_weight_api

urlpatterns = [
    path("scale/weight/", scale_weight_api),
]
