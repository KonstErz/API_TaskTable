from rest_framework import permissions


class CanChangeTask(permissions.BasePermission):
    """
    Object-level permission to only allow creators or performers of an task to edit it.
    """

    message = "Failure! You don't have permission to edit this task."

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user or obj.performer == request.user
