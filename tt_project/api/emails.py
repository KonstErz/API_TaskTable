from django.core.mail import send_mail


def basic_email_sender(task, title, recipients):

    body = 'Task name: ' + task.name + '\n' \
           + 'Specification: ' + task.specification + '\n' \
           + 'Due date: ' + str(task.due_date) + '\n' \
           + 'Creator: ' + task.creator.username + '\n' \
           + 'Performer: ' + task.performer.username + '\n' \
           + 'Status: ' + task.status

    send_mail(title, body, 'EMAIL_HOST_USER', recipients, fail_silently=False)


def comment_email_sender(task, comment, title, recipients):

    post_date = comment.post_date.strftime('%Y-%m-%d %H:%M')

    body = 'Task name: ' + task.name + '\n' \
           + 'Specification: ' + task.specification + '\n' \
           + 'Due date: ' + str(task.due_date) + '\n' \
           + 'Creator: ' + task.creator.username + '\n' \
           + 'Performer: ' + task.performer.username + '\n' \
           + 'Status: ' + task.status + '\n\n' \
           + 'New comment: ' + comment.description + '\n' \
           + 'Author: ' + comment.author.username + '\n' \
           + 'Posting date: ' + post_date

    send_mail(title, body, 'EMAIL_HOST_USER', recipients, fail_silently=False)
