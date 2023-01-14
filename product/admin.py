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


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo)
admin.site.register(Category)
admin.site.register(ProductComment)
