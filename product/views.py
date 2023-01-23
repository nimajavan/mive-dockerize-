from django.shortcuts import render, get_object_or_404
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import redis
from django.conf import settings
from django.db import connections
from rest_framework import status

# r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


@api_view(http_method_names=['GET'])
def get_product_list(request):
    try:
        products = Product.objects.all()
        serializer = ProductListSerializer(
            products, many=True, context={"request": request})
        return Response(serializer.data)
    except:
        return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def get_product_info(request, slug):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        product = ProductInfo.objects.get(
            product__slug=slug)
        if ip not in product.product.view.all():
            product_instance = Product.objects.get(slug=slug)
            product_instance.view.add(ViewIpAdress.objects.get(ip_address=ip))
            product_instance.total_view = product_instance.view.count()
            product_instance.save()
        seializer = ProductInfoSerializer(
            product, many=False, context={"request": request})
        return Response(seializer.data)
    except:
        return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def get_product_comments(request):
    try:
        data = request.data
        comments = ProductComment.objects.filter(
            product_id=data['id'], status='done')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)
    except:
        return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def send_comment(request):
    try:
        data = request.data
        commnet = ProductComment.objects.create(
            product_id=data['id'], user_id=request.user.id, body=data['body'])
        commnet.save()
        return Response(ProductCommentSerializer(commnet, many=False).data)
    except:
        return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class Like(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            product = get_object_or_404(Product, id=data['id'])
            if product.like.filter(id=request.user.id).exists():
                product.like.remove(request.user)
            else:
                product.like.add(request.user)

            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
