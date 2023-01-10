from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, ReplyTicket
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Ticket)
def set_ticket_status_signal(sender, instance, **kwargs):
    if ReplyTicket.objects.filter(ticket_id=instance.id).exists():
        obj = Ticket.objects.filter(
            id=instance.id).update(status='In Progress')


@receiver(post_save, sender=ReplyTicket)
def set_ticket_reply_status_signal(sender, instance, **kwargs):
    ticket = Ticket.objects.filter(id=instance.ticket.id).update(status='Done')
