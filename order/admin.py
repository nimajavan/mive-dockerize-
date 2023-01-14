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

    



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(PaymentHistory)
