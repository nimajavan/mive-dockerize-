from django.shortcuts import render, get_object_or_404
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


@api_view(http_method_names=['GET'])
def get_product_list(request):
    products = Product.objects.all()
    serializer = ProductListSerializer(
        products, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def get_product_info(request, slug):
    ip = request.META.get('REMOTE_ADDR')
    data = request.data
    viewChacker = view_checker(ip, data['id'])
    product = ProductInfo.objects.get(
        product_id=data['id'], product__slug=slug)
    if viewChacker:
        product_view = Product.objects.get(id=data['id'])
        product_view.views += 1
        product_view.save()

    seializer = ProductInfoSerializer(
        product, many=False, context={"request": request})
    return Response(seializer.data)


@api_view(http_method_names=['GET'])
def get_product_comments(request):
    data = request.data
    comments = ProductComment.objects.filter(
        product_id=data['id'], status='done')
    serializer = ProductCommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def send_comment(request):
    data = request.data
    commnet = ProductComment.objects.create(
        product_id=data['id'], user_id=request.user.id, body=data['body'])
    commnet.save()
    return Response(ProductCommentSerializer(commnet, many=False).data)


class Like(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        product = get_object_or_404(Product, id=data['id'])
        if product.like.filter(id=request.user.id).exists():
            product.like.remove(request.user)
        else:
            product.like.add(request.user)

        return Response(ProductListSerializer(product, many=False).data)


def view_checker(ip, p_id):
    if ViewIpAdress.objects.filter(product_id=p_id, ip_addr=ip).exists():
        return False
    else:
        ViewIpAdress.objects.create(product_id=p_id, ip_addr=ip)
        return True
