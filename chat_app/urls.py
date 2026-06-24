from django.urls import path
from .views import ChatUserListView, get_chat_history, upload_file_api, mark_messages_as_read

urlpatterns = [
    path('users/', ChatUserListView.as_view(), name='chat-users'),
    
    # 🎯 தப்பு இந்த வரியில தான் இருந்துச்சு, இப்போ 100% கரெக்டா மாத்தியாச்சு:
    path('history/<int:user_id>/', get_chat_history, name='chat-history'), 
    
    path('upload/', upload_file_api, name='chat-upload'),
    path('mark_read/<int:user_id>/', mark_messages_as_read, name='mark-read'), 
]