from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, UserStatus

User = get_user_model()

class UserChatStatusSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField(source='status.is_online', read_only=True)
    last_seen = serializers.DateTimeField(source='status.last_seen', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_online', 'last_seen']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    timestamp_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'receiver', 'content', 'file_upload', 'is_image', 'timestamp_formatted', 'is_read']

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime("%I:%M %p") # 04:30 PM WhatsApp Style