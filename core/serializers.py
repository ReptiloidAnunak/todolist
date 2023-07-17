
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs: dict) -> dict:
        if attrs["password_repeat"] != attrs['password']:
            raise serializers.ValidationError("Пароли должны совпадать")
        return attrs

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data=validated_data)
