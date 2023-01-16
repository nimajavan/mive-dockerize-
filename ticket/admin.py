from django.contrib import admin
from .models import *


class ReplyTickerInine(admin.StackedInline):
    model = ReplyTicket


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',
                    'user',
                    'status',
                    'shamsi_date_created', 'shamsi_date_updated']

    inlines = [ReplyTickerInine]
    list_filter = ['status']

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='ticket_permission').exists()

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='ticket_permission').exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='ticket_permission').exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='ticket_permission').exists()


admin.site.register(Ticket, TicketAdmin)
