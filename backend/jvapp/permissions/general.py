from rest_framework import permissions


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
