from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializerWithToken(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class GetFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'username_slug', 'first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'username_slug', 'first_name', 'last_name', 'email')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_user_data(self, user):
        serializer = GetFullUserSerializer(user)
        return serializer.data

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom data to the response
        user = self.user

        data['user'] = self.get_user_data(user)

        return data
