from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Signal to automatically create an authorization token for a user
    when creating a new user in the database.
    """

    if created:
        Token.objects.create(user=instance)


class Task(models.Model):
    """
    The Model represents a specific task to be completed,
    with a specific status, deadline, creator and performer.
    """

    name = models.CharField(unique=True, max_length=200,
                            help_text='Enter a task name')
    specification = models.TextField(help_text='Enter a task specification')
    due_date = models.DateField(null=True, blank=True,
                                help_text='Deadline for the task')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='task_creator')
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='task_performer')

    TASK_STATUS = (
        ('n', 'New'),
        ('w', 'In work'),
        ('c', 'Completed'),
    )

    status = models.CharField(max_length=1, choices=TASK_STATUS, default='n',
                              blank=True, help_text='Current task status')

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Model representing a comment against a task.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='task_comments')
    description = models.TextField(help_text='Enter a comment on the task here')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        if len(self.description) > 75:
            comment_string = self.description[:75] + '...'
        else:
            comment_string = self.description
        return comment_string
