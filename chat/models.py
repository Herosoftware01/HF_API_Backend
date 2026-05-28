from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    def __str__(self):
        return f'{self.user.username} Profile'


class Room(models.Model):
    ROOM_TYPES = [
        ('direct', 'Direct'),
        ('group', 'Group')
    ]

    name = models.CharField(max_length=200, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='direct')

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='rooms'
    )

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_rooms'
    )

    avatar = models.ImageField(upload_to='group_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, blank=True)

    def get_display_name(self, current_user):
        if self.room_type == 'group':
            return self.name
        other = self.members.exclude(id=current_user.id).first()
        return other.username if other else self.name

    def get_display_avatar(self, current_user):
        if self.room_type == 'group':
            return self.avatar.url if self.avatar else None
        other = self.members.exclude(id=current_user.id).first()
        if other and hasattr(other, 'profile') and other.profile.avatar:
            return other.profile.avatar.url
        return None

    def get_other_user(self, current_user):
        return self.members.exclude(id=current_user.id).first()

    def __str__(self):
        return self.name or f'Room {self.id}'


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField(blank=True)
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:40]}'