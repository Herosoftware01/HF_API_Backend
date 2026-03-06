from django.urls import path
from .views import *
from .import views


from .views import QcAdminMistakeAPIView, QcAdminMistakeDetailAPIView

urlpatterns = [
    path('qcadmin_mistakes/', QcAdminMistakeAPIView.as_view(), name='qcadmin_mistakes'),
    path('qcadmin_mistakes/<int:pk>/', QcAdminMistakeDetailAPIView.as_view(), name='qcadmin_mistake_detail'),
    path('lines/', LineAPIView.as_view()),
    path('lines/<int:pk>/', LineAPIView.as_view()),
]