from django.urls import path
from .views import ChatAPIView, index

urlpatterns = [
    path('', index, name='index'),
    path('api/chat/', ChatAPIView.as_view(), name='chat_api'),
]
