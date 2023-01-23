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
        'total_view',
        'slug',
    ]
    list_filter = [
        'available',
        'total_like'
    ]
    search_fields = [
        'name'
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


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'user',
        'status',
        'shamsi_date_time'
    ]

    list_filter = [
        'status'
    ]

    def shamsi_date_time(self, obj):
        return obj.shamsi_date_time()

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo)
admin.site.register(Category)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ViewIpAdress)
