from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'paid',
        'create',
        'discount',
        'first_name',
        'last_name',
        'phone',
        'sent',
    ]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(PaymentHistory)
