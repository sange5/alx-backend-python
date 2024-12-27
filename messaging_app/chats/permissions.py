from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow users to access their own resources only.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
