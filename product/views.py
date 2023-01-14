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

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

@api_view(http_method_names=['GET'])
def get_product_list(request):
    try:
        products = Product.objects.all()
        try:
            view_dic = {}
            for key in r.keys('image*'):
                view_dic[key.split(':')[1]] = f'{r.get(key)}'
        except:
            pass
        serializer = ProductListSerializer(
            products, many=True, context={"request": request, 'views_dic': view_dic})
        return Response(serializer.data)
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def get_product_info(request, slug, id):
    try:
        viewChacker = view_checker(id)
        product = ProductInfo.objects.get(
            product_id=id, product__slug=slug)
        seializer = ProductInfoSerializer(
            product, many=False, context={"request": request, 'views': viewChacker})
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    # query timinig (debug)    
    for query in connections['default'].queries:
        print (f'{query} ====> {query["time"]}')
    return Response(seializer.data)


@api_view(http_method_names=['GET'])
def get_product_comments(request):
    try:
        data = request.data
        comments = ProductComment.objects.filter(
            product_id=data['id'], status='done')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)
    except:
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)


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

            return Response({'status':'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status':'bad request'}, status=status.HTTP_400_BAD_REQUEST)



def view_checker(p_id):
    total_views = r.incr(f'image:{p_id}:views')
    return total_views
