from django.urls import path
from . import views 

urlpatterns = [
    # FashionR API
    path('process_fashionr/', views.process_fashionr_view),

    path("cutplan/", views.cutplan_list),
    path("fashionr-results/", views.fashionr_results),
]
