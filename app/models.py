from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Task(models.Model):
    """
    The Model represents a specific task to be completed,
    with a specific status, deadline, creator and performer (one or many Users).
    """

    name = models.CharField(max_length=200, help_text='Enter a task name')
    specification = models.TextField(help_text='Enter a task specification')
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='task_creator')
    performer = models.ManyToManyField(User, related_name='task_performer')

    TASK_STATUS = (
        ('n', 'New'),
        ('w', 'In work'),
        ('c', 'Completed'),
    )

    status = models.CharField(max_length=1, choices=TASK_STATUS, default='n',
                              blank=True, help_text='Current task status')

    class Meta:
        ordering = ['due_date']

    def display_performer(self):
        """
        Creates a string for the Performer. This is required to display performer in Admin.
        """
        return ', '.join([user.username for user in self.performer.all()])

    display_performer.short_description = 'Performer'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])  # Под вопросом


class Comment(models.Model):
    """
    Model representing a comment against a task.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField(help_text='Enter a comment on the task here')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        if len(self.description) > 75:
            comment_string = self.description[:75] + '...'
        else:
            comment_string = self.description
        return comment_string