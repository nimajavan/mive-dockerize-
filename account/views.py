from .serializers import *
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import send_sms_code
from django.http import JsonResponse
from ticket.models import Ticket
from order.models import Order
from random import randint
from product.models import ProductComment
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import timedelta, datetime
from django.db import connections


class EmailRegisterToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return force_str(user.is_active) + force_str(user.id) + force_str(timestamp)


class MyCreatorTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyCreatorTokenView(TokenObtainPairView):
    serializer_class = MyCreatorTokenSerializer


class SetupProfile(APIView):

    allowed_methods = ['POST', 'PUT', 'GET']
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializers(
            data=request.data, instance=request.user.profile, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        serializer = ProfileSerializers(profile, context={"request": request})
        return Response(serializer.data)

@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response(UserSerializerWithToken(user, many=False).data)
        else:
            return Response(serializer.errors)
    except:
        return Response({'error':'متاسفانه مشکلی پیش اومده لطفا دوباره امتحان کن'})
        

@api_view(http_method_names=['POST'])
def user_register(request):
    data = request.data
    random_code = force_str(urlsafe_base64_decode(
        request.session.get('random_code')))
    old_time = force_str(urlsafe_base64_decode(
        request.session.get('code_time_stamp')))
    old_time = datetime.strptime(old_time.split(".")[0], '%Y-%m-%d %H:%M:%S')
    now_time = datetime.strptime(str(timezone.now()).split(".")[
                                 0], '%Y-%m-%d %H:%M:%S')
    code_time = now_time - old_time
    if data['code'] == random_code and code_time <= timedelta(seconds=120):
        user = User.objects.create(phone=request.session.get(
            'phone'), password=make_password(data['password']))

        user.is_active = True
        user.save()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    elif code_time > timedelta(seconds=120):
        return JsonResponse({'error': 'کد وارد شده منقضی شده است'})
    else:
        return JsonResponse({'error': ' کد وارد شده اشتباه است'})


@api_view(http_method_names=['POST'])
def phone_register(request):
    data = request.data
    random_code = 1000
    phone = f'0{data["phone"]}'
    code_time_stamp = timezone.now()
    request.session['code_time_stamp'] = urlsafe_base64_encode(
        force_bytes(code_time_stamp))
    request.session['random_code'] = urlsafe_base64_encode(
        force_bytes(random_code))
    request.session['phone'] = phone
    try:
        try:
            request.session['resend_code_time']
        except:
            request.session['resend_code_time'] = None

        if request.session['resend_code_time'] is None:
            request.session['resend_code_time'] = urlsafe_base64_encode(
                force_bytes(code_time_stamp))
            send_sms_code.delay(phone, str(random_code))
            res = {'success': 'کد تایید با موفقیت ارسال شد'}

        elif request.session['resend_code_time'] is not None:
            old_time = force_str(urlsafe_base64_decode(
            request.session.get('resend_code_time')))
            old_time = datetime.strptime(
                old_time.split(".")[0], '%Y-%m-%d %H:%M:%S')
            now_time = datetime.strptime(str(timezone.now()).split(".")[
                                        0], '%Y-%m-%d %H:%M:%S')
            resend_code_time = now_time - old_time

            if resend_code_time >= timedelta(minutes=2):
                request.session['resend_code_time'] = urlsafe_base64_encode(
                force_bytes(code_time_stamp))
                send_sms_code.delay(phone, random_code)
                res = {'success': 'کد تایید با موفقیت ارسال شد'}
            else:
                res = {'error':'wait until 2 minutes'}

    except:
        res = {'error': 'متاسفانه مشکلی پیش اومد, لطفا دوباره امتحان کن'}

    # for query in connections['default'].queries:
    #     print(query, query['time'])
    return JsonResponse(res)


@api_view(http_method_names=['GET'])
def admin_panel_information(request):
    order = Order.objects.filter(paid=True, sent=False).count()
    ticket = Ticket.objects.filter(status='In Progress').count()
    total_paid = Order.objects.filter(paid=True)
    comments = ProductComment.objects.filter(status='to do').count()
    price = 0
    for t_p in total_paid.iterator():
        price += t_p.total_price()
    context = {
        'ticket': ticket,
        'order': order,
        'total_paid': price,
        'comments': comments
    }

    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        state = request.GET.get('state')
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
            case 4:
                comments = ProductComment.objects.filter(
                    status='to do').count()
                context = {'comments': comments}

    # query timimg check
    # for query in connections['default'].queries:
    #     print(query, query['time'])

    return Response(context)
