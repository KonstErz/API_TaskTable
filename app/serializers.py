from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment
import datetime


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


class TaskCreationSerializer(serializers.Serializer):
    """
    Serializes the data for creation a new task.
    Conducts object- and field-level validation.
    """

    name = serializers.CharField(max_length=200)
    specification = serializers.CharField()
    due_date = serializers.DateField()
    performer = serializers.CharField()

    def validate_performer(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('there is no user with that username')

        return value

    def validate_name(self, value):
        if Task.objects.filter(name=value).exists():
            raise serializers.ValidationError('a task with the same name already exists, try a another name')

        return value

    def validate(self, values):
        if len(values['name']) > 200:
            raise serializers.ValidationError('task name must be no more than 200 characters')

        elif values['specification'] is None:
            raise serializers.ValidationError('task specification should be indicated')

        elif values['due_date'] < datetime.date.today():
            raise serializers.ValidationError("due date cannot be earlier than today's date")

        return values


class CommentAddingSerializer(serializers.Serializer):
    """
    Serializes the data for adding a comment to a task.
    Conducts field-level validation.
    """

    task_name = serializers.CharField(max_length=200)
    description = serializers.CharField()

    def validate_task_name(self, value):
        if not Task.objects.filter(name=value).exists():
            raise serializers.ValidationError('there is no task with that name')

        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'post_date']


class TaskSerializer(serializers.ModelSerializer):
    task_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'specification', 'due_date', 'creator', 'performer', 'status', 'task_comments']
