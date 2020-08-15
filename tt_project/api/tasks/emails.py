from __future__ import absolute_import, unicode_literals
from celery import shared_task
from api.models import Task, Comment
from django.core.mail import send_mail
import logging
import smtplib


TIME_LIMIT = 30
MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 5 * 60

WARNING_MESSAGE = '''Problems sending email!
Please check if the "Less secure apps" option is enabled in the "Security" tab in your Google account, 
and also check the correctness of the entered Email Address and Password in the project settings.
A retry to send the email will occur in 5 minutes.'''


@shared_task(name='tasktable.send_basic_email', ignore_result=True,
             bind=True, time_limit=TIME_LIMIT, max_retries=MAX_RETRIES,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def basic_email_sender(self, task_id: int, title: str):
    task = Task.objects.get(id=task_id)
    body = 'Task name: ' + task.name + '\n' \
           + 'Specification: ' + task.specification + '\n' \
           + 'Due date: ' + str(task.due_date) + '\n' \
           + 'Creator: ' + task.creator.username + '\n' \
           + 'Performer: ' + task.performer.username + '\n' \
           + 'Status: ' + task.status
    recipients = [task.creator.email, task.performer.email]
    try:
        send_mail(title, body, 'EMAIL_HOST_USER',
                  recipients, fail_silently=False)
    except smtplib.SMTPException as exc:
        logging.warning(WARNING_MESSAGE)
        self.retry(exc=exc)


@shared_task(name='tasktable.send_comment_email', ignore_result=True,
             bind=True, time_limit=TIME_LIMIT, max_retries=MAX_RETRIES,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def comment_email_sender(self, task_id: int, comment_id: int):
    task = Task.objects.get(id=task_id)
    comment = Comment.objects.get(id=comment_id)
    post_date = comment.post_date.strftime('%Y-%m-%d %H:%M')
    title = 'A new comment has been added to the task'
    body = 'Task name: ' + task.name + '\n' \
           + 'Specification: ' + task.specification + '\n' \
           + 'Due date: ' + str(task.due_date) + '\n' \
           + 'Creator: ' + task.creator.username + '\n' \
           + 'Performer: ' + task.performer.username + '\n' \
           + 'Status: ' + task.status + '\n\n' \
           + 'New comment: ' + comment.description + '\n' \
           + 'Author: ' + comment.author.username + '\n' \
           + 'Posting date: ' + post_date
    recipients = [task.creator.email, task.performer.email]
    try:
        send_mail(title, body, 'EMAIL_HOST_USER',
                  recipients, fail_silently=False)
    except smtplib.SMTPException as exc:
        logging.warning(WARNING_MESSAGE)
        self.retry(exc=exc)
