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


admin.site.register(Ticket, TicketAdmin)
