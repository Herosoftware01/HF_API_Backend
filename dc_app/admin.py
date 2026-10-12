from django.contrib import admin

from .models import ModuleMaster, RoleModulePermission


@admin.register(ModuleMaster)
class ModuleMasterAdmin(admin.ModelAdmin):
    list_display = (
        "module_id",
        "module_name",
        "path",
        "display_order",
        "is_active",
        "updated_at",
    )
    list_editable = (
        "display_order",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = (
        "module_id",
        "module_name",
        "description",
        "path",
    )
    ordering = (
        "display_order",
        "module_name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "module_id",
        "module_name",
        "is_enabled",
        "updated_at",
    )
    list_editable = ("is_enabled",)
    list_filter = (
        "is_enabled",
        "module__is_active",
    )
    search_fields = (
        "role",
        "module__module_id",
        "module__module_name",
    )
    list_select_related = ("module",)

    @admin.display(
        description="Module name",
        ordering="module__module_name",
    )
    def module_name(self, permission):
        return permission.module.module_name