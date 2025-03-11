from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read access to anyone, but only write access to admin users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow read access to anyone, write access to staff, and edit access to authors of their own content.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Staff can edit anything
        if request.user.is_staff:
            return True
            
        # Authors can edit their own content
        return obj.author == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read access to anyone, but only write access to the owner of an object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return obj.author == request.user or request.user.is_staff