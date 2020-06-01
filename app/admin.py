from django.contrib import admin
from .models import Task, Comment


class CommentInline(admin.TabularInline):
    """
    Used to show 'existing' task comments inline below associated tasks.
    """

    model = Comment
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Administration object for Task models.
    Defines:
        - fields to be displayed in list view (list_display)
        - orders fields in detail view (fields), grouping the date fields horizontally
        - adds task filters by status and due date
        - adds inline addition of task comments in task view (inlines)
    """

    list_display = ('name', 'specification', 'due_date', 'creator', 'display_performer', 'status')
    list_filter = ('status', 'due_date')
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Administration object for Comments models defines:
        - fields to be displayed in list view (list_display)
        - orders fields in detail view (fields), grouping the date fields horizontally
    """

    list_display = ('task', 'post_date', 'author', 'description')
