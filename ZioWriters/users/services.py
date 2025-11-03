from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture_url', 'last_login']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

from datetime import timedelta
from django.utils import timezone
from .models import PasswordResetCode
import random

def generate_6_digit_code():
    return str(random.randint(100000, 999999))

def create_password_reset_code(user):
    code = generate_6_digit_code()

    expires_at = timezone.now() + timedelta(minutes=10)
    PasswordResetCode.objects.create(user=user, code=code, expires_at=expires_at)
    return code