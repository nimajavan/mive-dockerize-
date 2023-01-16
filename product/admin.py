from django.contrib import admin
from .models import *


class ProductInfoInline(admin.StackedInline):
    model = ProductInfo


class ProductTagsInline(admin.StackedInline):
    model = ProductTags


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInfoInline, ProductTagsInline]
    list_display = [
        'id',
        'name',
        'available',
        'price',
        'special_offer',
        'total_like',
        'slug',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }

    def get_id_product(self, obj):
        return obj.id

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='product_permission').exists()

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='product_permission').exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='product_permission').exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='product_permission').exists()


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo)
admin.site.register(Category)
admin.site.register(ProductComment)
