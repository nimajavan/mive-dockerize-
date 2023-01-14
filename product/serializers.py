from rest_framework import serializers
from .models import *
from account.models import Profile
import json


class ProductTagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductTags
        fields = ['tags']


class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField('get_image_url')
    tags = ProductTagsSerializers(many=True, read_only=True)
    views = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        depth = 1
        fields = ['id', 'name', 'image', 'available', 'category',
                  'price', 'special_offer', 'total_like', 'tags', 'views']

    def get_views(self, obj):
        try:
            view = self.context.get('views_dic')
            return view[str(obj.id)]
        except:
            return '0'

    def get_id(self, obj):
        return obj.id

    def get_image_url(self, obj):
        request = self.context.get('request')
        image = obj.image.url
        return request.build_absolute_uri(image)


class ProductListInInfoSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField('get_image_url')
    tags = ProductTagsSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        depth = 1
        fields = ['id', 'name', 'image', 'available', 'category',
                  'price', 'special_offer', 'total_like', 'tags']

    def get_id(self, obj):
        return obj.id

    def get_image_url(self, obj):
        request = self.context.get('request')
        image = obj.image.url
        return request.build_absolute_uri(image)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductListInInfoSerializer(many=False)
    views = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductInfo
        fields = [
            'product',
            'views',
            'text',
            'english_name',
            'weight',
            'country',
            'taste',
            'energy',
            'protein',
            'fat',
            'how_to_use',
        ]
    
    def get_views(self, obj):
        return self.context.get('views')


class ProductCommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductComment
        fields = ['product_id', 'user_id', 'body', 'name']

    def get_name(self, obj):
        name = None
        try:
            name = Profile.objects.get(user_id=obj.user.id).name
        except:
            pass
        if name == None:
            name = 'ناشناس'
        return name
