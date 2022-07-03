from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object and admins to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff is True


class IsThisUserOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object and admins to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff is True
