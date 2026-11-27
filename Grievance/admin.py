from django.contrib import admin
from .models import CategoryMaster, SubCategoryMaster


@admin.register(CategoryMaster)
class CategoryMasterAdmin(admin.ModelAdmin):
    list_display = (
        'category_id',
        'category_name',
        'role',
        'active',
    )

    list_filter = ('active', 'role')
    search_fields = ('category_name', 'role')
    list_editable = ('active',)


@admin.register(SubCategoryMaster)
class SubCategoryMasterAdmin(admin.ModelAdmin):
    list_display = (
        'subcategory_id',
        'subcategory_name',
        'category',
        'active',
    )

    list_filter = ('active', 'category')
    search_fields = ('subcategory_name', 'category__category_name')
    list_editable = ('active',)
    autocomplete_fields = ('category',)