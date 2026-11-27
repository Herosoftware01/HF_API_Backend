from django.urls import path
from . import views 

urlpatterns = [

    
    path("category/", views.Category_API),
    path("category/<int:pk>/", views.Category_Detail_API),

    path("subcategory/", views.SubCategory_API),
    path("subcategory/<int:pk>/", views.SubCategory_Detail_API),


]