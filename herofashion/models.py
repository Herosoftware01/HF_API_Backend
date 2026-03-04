from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="menu_icons/", blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, related_name="submenus", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.name


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
