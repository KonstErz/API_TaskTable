from rest_framework.views import APIView
from .serializers import (RegistrationSerializer, LoginSerializer,
                          TaskCreationSerializer, CommentAddingSerializer)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .models import Task, Comment


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


class TaskCreationView(APIView):
    """
    The View class creates a new task with the default status 'New'.
    Requesting user will be the creator.
    Returns the name of the new task.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        creator = User.objects.filter(username=request.user).first()
        name = serializer.validated_data['name']
        specification = serializer.validated_data['specification']
        due_date = serializer.validated_data['due_date']
        performer = User.objects.filter(username=serializer.validated_data['performer']).first()

        task = Task.objects.create(name=name, specification=specification, due_date=due_date,
                                   creator=creator, performer=performer, status='n')

        return Response({'task created successfully': task.name})


class CommentAddingView(APIView):
    """
    The View class implements adding a comment to the specified task.
    Requesting user will be the author of the comment.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentAddingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = Task.objects.filter(name=serializer.validated_data['task_name']).first()
        description = serializer.validated_data['description']
        author = User.objects.filter(username=request.user).first()

        comment = Comment.objects.create(task=task, description=description, author=author)

        return Response({'success': f"Comment on the task '{task}' was published successfully"}, 200)
