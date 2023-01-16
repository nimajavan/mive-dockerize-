from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    try:
        data = request.data
        ticket = Ticket.objects.create(
            user_id=request.user.id, title=data['title'], body=data['body'])
        serializer = TicketSerializers(ticket, many=False)
        return Response(serializer.data)
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def show_all_ticket(request):
    print(request.user.groups.filter(name='ticket-admin').exists())
    try:
        ticket = Ticket.objects.filter(user=request.user.id)
        serializer = TicketSerializers(ticket, many=True)
        return Response(serializer.data)
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def show_single_ticket(request):
    try:
        data = request.data
        ticket = Ticket.objects.get(id=data['id'], user_id=request.user.id)
        serializer = TicketSingleShowSerializers(ticket, many=False)
        return Response(serializer.data)
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)
