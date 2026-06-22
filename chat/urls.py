from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/<int:room_id>/', views.room_view, name='room'),
    path('chat/start/<int:user_id>/', views.start_direct_chat, name='start_direct'),
    path('chat/create-group/', views.create_group, name='create_group'),
    path('chat/<int:room_id>/upload/', views.upload_file, name='upload_file'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('api/status/', views.user_status_api, name='user_status'),
    path('messages/<int:room_id>/', views.messages_api, name='messages_api'),
    path('send/<int:room_id>/', views.send_message, name='send_message'),
    path("html-to-image/", views.html_to_image, name="html_to_image"),

    
]
