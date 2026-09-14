from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="menu_icons/", blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

   
class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, related_name="submenus", on_delete=models.CASCADE)

    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    default_submenu = models.ForeignKey(
        SubMenu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select default submenu to open after login"
    )


class RoleMenuPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'menu')

    def __str__(self):
        return f"{self.role} - {self.menu}"

class RoleSubMenuPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    submenu = models.ForeignKey(SubMenu, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'submenu')


class LoginLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="login_logs"
    )

    user_id_logged = models.IntegerField(
        null=True,
        blank=True
    )

    username = models.CharField(
        max_length=150
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    password_entered = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user_id_logged} - {self.username} - {self.status}"

