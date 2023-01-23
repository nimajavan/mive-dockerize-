from django.shortcuts import render
from .models import *
import logging
from django.http import HttpResponse, Http404
from django.urls import reverse
from rest_framework.decorators import APIView, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializers
import requests as req
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone


class GetOrderItem(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        order = Order.objects.filter(user=request.user)
        return Response(OrderSerializers(order, many=True).data)

    def post(self, request):
        data = request.data
        order = Order.objects.create(
            user=request.user, first_name=data['name'], last_name=data['last_name'], phone=request.user.phone, address=data['address'], delivery_date=data['delivery_date'], postal_code=data['postal_code'])
        if data['coupon_code']:
            coupon_checker(data['coupon_code'], order.id)
        for cart_item in data['cart_item']:
            order_item = OrderItem.objects.create(
                order_id=order.id, user=request.user, product_id=cart_item['product_id'], quantity=cart_item['quantity'])
        return Response(OrderSerializers(order, many=False).data)

def coupon_checker(code, order_id):
    try:
        coupun = Coupon.objects.get(code=code)
        now_time = timezone.now()
        if now_time >= coupun.start and now_time <= coupun.end:
            order = Order.objects.get(id=order_id)
            order.discount = coupun.discount
            order.save()
    except:
        return Response({'error':'چنین توکنی موجود نیست'})



@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def create_payment_url(request):
    try:
        data = request.data
        order = Order.objects.get(id=data['order_id'])
        headers = {
            'Content-Type': settings.CONTEXNT_TYPE,
            'X-API-KEY': settings.X_API_KEY,
            'X-SANDBOX': settings.X_SANDBOX,
        }

        payload = {
            'order_id': order.id,
            'amount': order.total_price(),
            'name': 'test',
            'phone': order.phone,
            'mail': 'test@gmail.com',
            'desc': 'test_desc',
            'callback': f'{settings.HOST_ADDRESS}/api/v1/verify_peyment/'
        }

        record = PaymentHistory.objects.create(
            order_id=data['order_id'], amount=int(order.total_price()))

        r = req.post('https://api.idpay.ir/v1.1/payment',
                     headers=headers, data=json.dumps(payload))

        result = r.json()

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

        return Response(r.json())

    except:
        return Response({'متاسفانه مشکلی به وجود اومده'})


@csrf_exempt
@api_view(http_method_names=['POST'])
def payment_return(request):
    pid = request.POST.get('id')
    status = request.POST.get('status')
    pidtrack = request.POST.get('track_id')
    order_id = request.POST.get('order_id')
    amount = request.POST.get('amount')
    card = request.POST.get('card_no')
    date = request.POST.get('date')

    if PaymentHistory.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

        payment = PaymentHistory.objects.get(payment_id=pid, amount=amount)
        payment.status = status
        payment.date = str(date)
        payment.card_number = card
        payment.idpay_track_id = pidtrack
        payment.save()

        if str(status) == '10':
            headers = {
                'Content-Type': settings.CONTEXNT_TYPE,
                'X-API-KEY': settings.X_API_KEY,
                'X-SANDBOX': settings.X_SANDBOX,
            }
            payload = {
                'id': pid,
                'order_id': payment.order_id
            }

            r = req.post('https://api.idpay.ir/v1.1/payment/verify',
                         headers=headers, data=json.dumps(payload))
            result = r.json()

            if 'status' in result:

                payment.status = result['status']
                payment.bank_track_id = result['payment']['track_id']
                payment.save()
                order = Order.objects.get(id=order_id)
                if result['status'] == 100:
                    order.paid = True
                    order.save()
                return render(request, 'order/return_payment.html', {'status': result['status'], 'bank_track_id': payment.bank_track_id})

            else:
                txt = result['status']

        else:
            txt = "Error Code : " + \
                str(status) + "   |   " + "Description : " + \
                result.get_status(status)

    else:
        txt = "Order Not Found"

    return render(request, 'order/return_payment.html', {'status': txt})


@api_view(http_method_names=['POST'])
def payment_check(request):
    try:
        pk = request.data['pk']

        payment = PaymentHistory.objects.get(pk=pk)
        headers = {
            'Content-Type': settings.CONTEXNT_TYPE,
            'X-API-KEY': settings.X_API_KEY,
            'X-SANDBOX': settings.X_SANDBOX,
        }
        payload = {
            'id': payment.payment_id,
            'order_id': payment.order_id
        }

        r = req.post('https://api.idpay.ir/v1.1/payment/inquiry',
                     headers=headers, data=json.dumps(payload))
        result = r.json()

        if 'status' in result:

            payment.status = result['status']
            payment.idpay_track_id = result['track_id']
            payment.bank_track_id = result['payment']['track_id']
            payment.card_number = result['payment']['card_no']
            payment.date = str(result['date'])
            payment.save()

        return Response({'txt': result['message']})

    except:
        return Response({'txt': 'متاسفانه مشکلی به وجود آمده'})
