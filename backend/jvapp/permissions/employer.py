from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from jvapp.models import JobVyneUser


class IsAdminOrEmployerOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        return any((
            user.user_type_bits & JobVyneUser.USER_TYPE_ADMIN,
            user.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYER,
        ))


class IsAdminOrEmployerPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        return any((
            user.user_type_bits & JobVyneUser.USER_TYPE_ADMIN,
            user.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYER,
        ))
