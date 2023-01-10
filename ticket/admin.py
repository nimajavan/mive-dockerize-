from django.contrib import admin
from .models import *


class ReplyTickerInine(admin.StackedInline):
    model = ReplyTicket


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',
                    'user',
                    'status',
                    'persian_calender_created', 'persian_calender_updated']

    inlines = [ReplyTickerInine]
    list_filter = ['status']


admin.site.register(Ticket, TicketAdmin)
