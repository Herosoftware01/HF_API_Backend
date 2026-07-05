from django.urls import path
from .views import (
    ChatUserListView, 
    UserProfileView,
    ConversationsListView,
    GroupListView, 
    GroupDetailView, 
    BroadcastListView, 
    BroadcastDetailView, 
    get_chat_history, 
    upload_file_api, 
    delete_message_api,
    mark_messages_as_read
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', ChatUserListView.as_view(), name='chat-users'),
    path('conversations/', ConversationsListView.as_view(), name='chat-conversations'),
    
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    
    path('broadcasts/', BroadcastListView.as_view(), name='broadcast-list'),
    path('broadcasts/<int:pk>/', BroadcastDetailView.as_view(), name='broadcast-detail'),
    
    path('history/<int:user_id>/', get_chat_history, name='chat-history'), 
    
    path('upload/', upload_file_api, name='chat-upload'),
    path('messages/<int:message_id>/delete/', delete_message_api, name='message-delete'),
    path('mark_read/<int:user_id>/', mark_messages_as_read, name='mark-read'), 
]