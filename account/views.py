from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import send_sms_code
from django.http import JsonResponse
from ticket.models import Ticket
from order.models import Order
from django.db import connections
from random import randint


class MyCreatorTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyCreatorTokenView(TokenObtainPairView):
    serializer_class = MyCreatorTokenSerializer


@api_view(http_method_names=['POST'])
def user_register(request):
    data = request.data
    if data['code'] == str(request.session.get('random_code')):
        user = User.objects.create(phone=request.session.get(
            'phone'), password=make_password(data['password']))
        user.is_active = True
        user.save()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    else:
        return JsonResponse({'error': ' کد وارد شده اشتباه است'})


class SetupProfile(APIView):

    allowed_methods = ['POST', 'PUT']
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializers(
            data=request.data, instance=request.user.profile, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(http_method_names=['POST'])
def phone_register(request):
    data = request.data
    random_code = randint(100, 10000)
    phone = f'0{data["phone"]}'
    request.session['random_code'] = random_code
    request.session['phone'] = phone
    try:
        send_sms_code.delay(phone, random_code)
        res = {'success': 'کد تایید با موفقیت ارسال شد'}
    except:
        res = {'error': 'متاسفانه مشکلی پیش اومد, لطفا دوباره امتحان کن'}
    return JsonResponse(res)


@api_view(http_method_names=['GET'])
def admin_panel_information(request):
    order = Order.objects.filter(paid=True, sent=False).count()
    ticket = Ticket.objects.filter(status='In Progress').count()
    total_paid = Order.objects.filter(paid=True)
    price = 0
    for t_p in total_paid.iterator():
        price += t_p.total_price()
    context = {
        'ticket': ticket,
        'order': order,
        'total_paid': price
    }

    # ajax method
    state = request.GET.get('state')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        match state:
            case 1:
                order = Order.objects.filter(paid=True, sent=False).count()
                context = {'order': order}
            case 2:
                ticket = Ticket.objects.filter(status='In Progress').count()
                context = {'ticket': ticket}
            case 3:
                total_paid = Order.objects.filter(paid=True)
                price = 0
                for t_p in total_paid.iterator():
                    price += t_p.total_price()
                context = {'total_paid': price}

    # query timimg check
    # for query in connections['default'].queries:
    #     print(query, query['time'])

    return Response(context)
