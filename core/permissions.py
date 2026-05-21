from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    # Anyone can read (GET), only admins can write (POST, PUT, DELETE)
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # allow read-only requests for everyone
        return request.user and request.user.is_staff  # allow write only if user is admin
