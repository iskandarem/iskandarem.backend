from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    """
    Custom permission to only allow authors of a post to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user
    

class LikePermission(BasePermission):
    """
    Custom permission to allow users to like a post.
    """
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated
        return True  # Allow GET requests for viewing likes

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to perform write operations.
    """
    def has_permission(self, request, view):
        if request.method in ['HEAD', 'GET', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated