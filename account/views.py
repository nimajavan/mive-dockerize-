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
    random_code = 333
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
def phone_r(request):
    r = request.session.get('phone')
    p = {'p': r}
    return JsonResponse(p)


@api_view(http_method_names=['GET'])
def admin_panel_information(request):
    ticket = Ticket.objects.filter(status='In Progress').count()
    order = Order.objects.filter(paid=True, sent=False).count()
    total_paid = Order.objects.filter(paid=True)
    price = 0
    for t_p in total_paid:
        price += t_p.total_price()
    context = {
        'ticket': ticket,
        'order': order,
        'total_paid': price
    }
    return Response(context)
