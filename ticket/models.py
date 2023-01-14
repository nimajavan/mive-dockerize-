from django.db import models
from account.models import User
from jalali_date import datetime2jalali, date2jalali


class TicketStatus(models.TextChoices):
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'


class Ticket(models.Model):
    title = models.CharField(max_length=100, verbose_name='تایتل')
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
    status = models.CharField(
        max_length=25, choices=TicketStatus.choices, default=TicketStatus.IN_PROGRESS, verbose_name='وضعیت', db_index=True)
    body = models.TextField(verbose_name='متن تیکت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return str(self.title)

    def shamsi_date_created(self):
        return datetime2jalali(self.created_at)

    def shamsi_date_updated(self):
        return datetime2jalali(self.updated_at)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class ReplyTicket(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='reply_ticket', verbose_name='تیکت')
    reply_body = models.TextField(verbose_name='متن پاسخ')
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    persian_calender_created = models.DateTimeField()
    persian_calender_updated = models.DateTimeField()

    def persian_calender_created(self):
        return datetime2jalali(self.created_at)

    def persian_calender_updated(self):
        return datetime2jalali(self.updated_at)

    class Meta:
        verbose_name = 'جواب تیکت'
        verbose_name_plural = 'جواب تیکت ها'
