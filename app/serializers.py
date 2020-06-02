from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment


class RegistrationSerializer(serializers.Serializer):
    """
    Serializes the data for registering a new user.
    Conducts field-level validation.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('username already exist')

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exist')

        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializes data for logging the user in the system.
    """

    username = serializers.CharField()
    password = serializers.CharField()
