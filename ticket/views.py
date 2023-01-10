from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(http_method_names=['POST'])
def create_ticket(request):
    data = request.data
    ticket = Ticket.objects.create(
        user_id=request.user.id, title=data['title'], body=data['body'])
    serializer = TicketSerializers(ticket, many=False)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def show_all_ticket(request):
    ticket = Ticket.objects.filter(user=request.user.id)
    serializer = TicketSerializers(ticket, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def show_single_ticket(request):
    data = request.data
    ticket = Ticket.objects.get(id=data['id'], user_id=request.user.id)
    serializer = TicketSingleShowSerializers(ticket, many=False)
    return Response(serializer.data)
