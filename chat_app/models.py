from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# User-oda Online/Last Seen status-ai track seiya
class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"


# Chat Message Model (Supports Text & Files/Images)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_received_messages")
    content = models.TextField(blank=True, null=True) # Text message-ku
    
    # Image/File Upload features
    file_upload = models.FileField(upload_to="chat_files/", blank=True, null=True)
    is_image = models.BooleanField(default=False)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}"