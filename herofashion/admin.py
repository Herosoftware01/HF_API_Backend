from django.contrib import admin
from .models import *

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Menu)
admin.site.register(SubMenu)
admin.site.register(RoleSubMenuPermission)
admin.site.register(RoleMenuPermission)