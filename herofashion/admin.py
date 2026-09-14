from django.contrib import admin
from .models import *

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Menu)
admin.site.register(SubMenu)
admin.site.register(RoleSubMenuPermission)
admin.site.register(RoleMenuPermission)


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        "user_id_logged",
        "username",
        "ip_address",
        "login_time",
        "status",
        "password_entered",
    )

    list_filter = (
        "status",
        "login_time",
    )

    search_fields = (
        "username",
        "ip_address",
    )

    ordering = ("-login_time",)
