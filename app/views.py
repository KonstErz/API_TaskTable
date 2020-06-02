from rest_framework.views import APIView
from .serializers import (RegistrationSerializer, LoginSerializer)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


class RegistrationView(APIView):
    """
    The View class creates a new user and its authorization token.
    Returns the id of the new user.
    """

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)

        Token.objects.create(user=user)

        return Response({'user_id': user.id})


class LoginView(APIView):
    """
    The View class logs the user in the system and returns an authorization token,
    if such a user exists in the system.
    Returns status code 400 for invalid data.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        if user is not None:
            login(request, user)
            return Response({'Authorization: Token': user.auth_token.key})
        else:
            return Response({'error': 'username or password invalid'}, 400)


class LogoutView(APIView):
    """
    The View class logs the user out using the POST request method.
    """

    def post(self, request):
        logout(request)
        return Response({'success': 'Sucessfully logged out'}, 200)
