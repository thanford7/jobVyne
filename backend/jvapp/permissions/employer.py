from rest_framework import permissions

from jvapp.models import JobVyneUser


class IsAdminOrEmployerOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        return any((
            user.user_type_bits & JobVyneUser.USER_TYPE_ADMIN,
            user.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYER,
        ))
