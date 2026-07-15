from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Privacy and User Status Settings
class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    # Privacy controls
    hide_last_seen = models.BooleanField(default=False)
    hide_profile_photo = models.BooleanField(default=False)
    hide_read_receipts = models.BooleanField(default=False)
    blocked_users = models.ManyToManyField(User, related_name="blocked_by", blank=True)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"


# Group Chat Model
class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="group_avatars/", blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_groups")
    admins = models.ManyToManyField(User, related_name="admin_of_groups")
    members = models.ManyToManyField(User, related_name="member_of_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Broadcast List Model
class BroadcastList(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="broadcast_lists")
    members = models.ManyToManyField(User, related_name="broadcast_members")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Enhanced Message Model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sent_messages")
    # Receiver can be a single user, a group, or a broadcast list
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_received_messages", null=True, blank=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    broadcast = models.ForeignKey(BroadcastList, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    
    content = models.TextField(blank=True, null=True)
    
    # Message Features
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="replies")
    is_forwarded = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ManyToManyField(User, related_name="deleted_messages", blank=True)
    disappearing_time = models.IntegerField(null=True, blank=True, help_text="Time in seconds before deletion")
    
    # Media & Attachments
    file_upload = models.FileField(upload_to="chat_files/", blank=True, null=True)
    is_image = models.BooleanField(default=False)
    voice_note = models.FileField(upload_to="chat_voice/", blank=True, null=True)
    short_video = models.FileField(upload_to="chat_video/", blank=True, null=True)
    document = models.FileField(upload_to="chat_docs/", blank=True, null=True)
    
    # Location & Contacts
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)
    contact_data = models.JSONField(null=True, blank=True, help_text="Store vCard or contact info")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        target = self.receiver.username if self.receiver else (self.group.name if self.group else "Broadcast")
        return f"{self.sender.username} to {target}"


# Group Read Receipts (Tracking who read what in a group)
class MessageReadReceipt(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="read_receipts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="read_messages")
    read_at = models.DateTimeField(auto_now_add=True)


# Message Reactions (Emojis)
class MessageReaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')


# Polls Implementation
class Poll(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name="poll")
    question = models.CharField(max_length=255)
    multiple_answers = models.BooleanField(default=False)

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

class PollVote(models.Model):
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('option', 'user')