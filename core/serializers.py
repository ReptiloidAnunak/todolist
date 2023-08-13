
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from core.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.IntegerField(read_only=True)
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs: dict) -> dict:
        """Проверяет совпадение вводов паролей при регистрации"""
        if attrs["password_repeat"] != attrs['password']:
            raise serializers.ValidationError("Пароли должны совпадать")
        return attrs

    def create(self, validated_data: dict) -> None:
        """Создает запись пользователя в базе данных
        с проверенным и захэшироанным паролем"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data=validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdatePwdSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']
