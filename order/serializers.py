from .models import *
from rest_framework import serializers


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'user_id', 'product_id', 'quantity']


class OrderSerializers(serializers.ModelSerializer):
    order_item = OrderItemSerializers(many=True, read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_fields = ['order_item', 'price']

    def get_price(self, obj):
        return obj.total_price()
