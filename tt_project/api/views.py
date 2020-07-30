from rest_framework.views import APIView
from .serializers import (RegistrationSerializer, LoginSerializer,
                          TaskCreationSerializer, CommentAddingSerializer,
                          TaskSerializer, TaskListSerializer,
                          TaskDetailSerializer, CommentSerializer)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .models import Task, Comment
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from .emails import basic_email_sender, comment_email_sender


class RegistrationView(APIView):
    """
    The View class creates a new user and its authorization token.
    Returns the authorization token of the new user.
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

        context = {
            'Success. Your authorization token': user.auth_token.key
        }

        return Response(context)


class LoginView(APIView):
    """
    The View class logs the user in the system and returns its id,
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
            return Response({'Login successful. Your user id': user.id})
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
    Returns the id of the new task.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        creator = User.objects.filter(username=request.user).first()
        name = serializer.validated_data['name']
        specification = serializer.validated_data['specification']
        due_date = serializer.validated_data['due_date']
        performer = User.objects.filter(username=serializer.validated_data[
            'performer']).first()

        task = Task.objects.create(name=name, specification=specification,
                                   due_date=due_date, creator=creator,
                                   performer=performer, status='n')

        context = {
            f"task '{task.name}' created successfully. Task id": task.id
        }

        return Response(context)


class CommentAddingView(APIView):
    """
    The View class implements adding a comment to the specified task.
    Requesting user will be the author of the comment.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentAddingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = Task.objects.filter(name=serializer.validated_data[
            'task_name']).first()
        description = serializer.validated_data['description']
        author = User.objects.filter(username=request.user).first()

        Comment.objects.create(task=task, description=description,
                               author=author)

        context = {
            'success': 'Comment on the task was published successfully'
        }

        return Response(context, 200)


class TaskViewSet(viewsets.ModelViewSet):
    """
    This ModelViewSet class implements the display of the list of tasks
    and detailed information about the task (including all comments on it).
    Allows to create a new task, edit an existing task, and add comments to the task.
    Includes Search Filter by task name and performer name.
    Requesting user will be the creator of the task and author of the comment.
    When creating/editing a task or adding a new comment to a task,
    an email is sent with information to the creator and performer.
    """

    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all().select_related(
        'creator', 'performer').prefetch_related('task_comments').order_by(
        '-due_date')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'performer__username']

    def perform_create(self, serializer):
        serializer.save(creator=serializer.context['request'].user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        elif self.action == 'add_comment':
            return CommentSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        if not self.get_object():
            return Response({'error': 'task does not exists'}, 404)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, task_id=pk)

        task = Task.objects.filter(id=pk).first()
        comment = Comment.objects.filter(
            task=task,
            author=request.user,
            description=request.data['description']
        ).first()
        recipients = [task.creator.email, task.performer.email]
        title = 'A new comment has been added to the question'
        comment_email_sender(task=task, comment=comment,
                             title=title, recipients=recipients)

        return Response({'status': 'comment added'}, 201)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        task = Task.objects.filter(id=response.data['id']).first()
        recipients = [task.creator.email, task.performer.email]
        basic_email_sender(task=task,
                           title='A new task has been created',
                           recipients=recipients)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        task = Task.objects.filter(id=response.data['id']).first()
        recipients = [task.creator.email, task.performer.email]
        basic_email_sender(task=task,
                           title='Task has been changed',
                           recipients=recipients)
        return response
