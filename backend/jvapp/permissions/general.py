from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthenticatedOrPostOrRead(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS + ('POST',):
            return True
        
        user = request.user
        return user and user.is_authenticated
   
 
class IsAuthenticatedOrPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        
        user = request.user
        return user and user.is_authenticated
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
    
    
class IsAdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_admin)
        )
