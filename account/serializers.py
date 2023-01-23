from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

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
    class Meta:
        model = Profile
        fields = [
            'name',
            'last_name',
            'profile_image'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required = True)
    password = serializers.CharField(required = True, validators=[validate_password])
    password_2 = serializers.CharField(required = True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError({'status': 'پسورد ها همخوانی ندارند'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'status':'پسورد قدیمی همخوانی ندارد'})
        return value

