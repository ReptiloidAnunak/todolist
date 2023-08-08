
from rest_framework import serializers
from core.models import User
from bot.models import TgUser


class TgUserVerificationSerializer(serializers.ModelSerializer):

    def validate_verification_code(self, verification_code):
        if not TgUser.objects.filter(
                verification_code=verification_code).exists():
            raise serializers.ValidationError("Код неверный")
        return verification_code

    class Meta:
        id = serializers.IntegerField(read_only=True)
        model = User
        fields = ['verification_code']

