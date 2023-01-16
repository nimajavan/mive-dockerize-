from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'paid',
        'discount',
        'first_name',
        'last_name',
        'phone',
        'sent',
        'shamsi_date',
    ]
    def shamsi_date(self, obj):
        return obj.shamsi_date_time()

    inlines = [OrderItemInline]

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='order_permission').exists()

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='order_permission').exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='order_permission').exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='order_permission').exists()

    



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(PaymentHistory)
