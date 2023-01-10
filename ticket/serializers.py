from .models import *
from rest_framework import serializers


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class ReplyTickerSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReplyTicket
        fields = ['reply_body', 'created_at',
                  'updated_at']


class TicketSingleShowSerializers(serializers.ModelSerializer):
    reply_ticket = ReplyTickerSerializers(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        extra_field = ['reply_ticket']
