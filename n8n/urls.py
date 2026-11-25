from django.urls import path
from . import views

urlpatterns = [
    path('ws_attendance/', views.ws_attendance, name='ws_attendance'), 
    path('liveprdn/', views.liveprdn, name='liveprdn'),
    path("html-to-image/", views.html_to_image, name="html_to_image"),
    path(
        "html-to-pdf/",
        views.html_to_pdf,
        name="html_to_pdf"
    ),
]