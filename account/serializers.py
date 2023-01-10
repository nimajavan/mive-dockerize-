from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'is_admin']

    def get_id(self, obj):
        return obj.id

    def get_is_admin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'is_admin', 'token']

    def get_id(self, obj):
        return obj.id

    def get_is_admin(self, obj):
        return obj.is_staff

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ProfileSerializers(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField('get_photo_url')

    class Meta:
        model = Profile
        fields = '__all__'

    def get_photo_url(self, obj):
        request = self.context.get('request')
        image = obj.profile_image.url
        return request.build_absolute_uri(image)
