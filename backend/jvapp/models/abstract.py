from enum import Enum

from django.db import models

from jvapp.utils.logger import getLogger

__all__ = (
    'ALLOWED_UPLOADS_FILE', 'ALLOWED_UPLOADS_VIDEO', 'ALLOWED_UPLOADS_IMAGE', 'ALLOWED_UPLOADS_ALL',
    'AuditFields', 'OwnerFields', 'JobVynePermissionsMixin'
)


logger = getLogger()


ALLOWED_UPLOADS_FILE = ['doc', 'docx', 'pdf', 'pages', 'gdoc']
ALLOWED_UPLOADS_VIDEO = ['mp4', 'm4v', 'mov', 'wmv', 'avi', 'mpg', 'webm']
ALLOWED_UPLOADS_IMAGE = ['png', 'jpeg', 'jpg', 'gif']
ALLOWED_UPLOADS_ALL = ALLOWED_UPLOADS_IMAGE + ALLOWED_UPLOADS_VIDEO + ALLOWED_UPLOADS_FILE


class AuditFields(models.Model):
    created_dt = models.DateTimeField()
    modified_dt = models.DateTimeField()

    class Meta:
        abstract = True
        
        
class OwnerFields(models.Model):
    created_user = models.ForeignKey('JobVyneUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_user')
    modified_user = models.ForeignKey('JobVyneUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_modified_user')
    
    class Meta:
        abstract = True
 
 
class PermissionTypes(Enum):
    CREATE = 'create'
    EDIT = 'edit'
    DELETE = 'delete'

    
class JobVynePermissionsMixin:
    """Override to give object level permissions
    """
    
    @classmethod
    def jv_filter_perm(cls, user, query):
        """Checks whether some or all query objects have been filtered out due to permission constraints
        Don't override this method. Use jv_filter_perm_query instead
        """
        starting_length = len(query)
        query = cls._jv_filter_perm_query(user, query)
        ending_length = len(query)
        
        if starting_length and not ending_length:
            raise PermissionError('You do not have permission to view this object')
        
        if starting_length != ending_length:
            logger.warn(f'User (ID={user.id}) does not have access to all query objects')
            
        return query
    
    @classmethod
    def _jv_filter_perm_query(cls, user, query):
        """ Filter an existing query_set based on user's access
        """
        return query
    
    def jv_check_permission(self, permission_type: PermissionTypes, user):
        """Check whether the user has permission to operate on an object
        Don't override this method.
        """
        if permission_type == PermissionTypes.CREATE.value:
            has_permission = self._jv_can_create(user)
        elif permission_type == PermissionTypes.EDIT.value:
            has_permission = self._jv_can_edit(user)
        elif permission_type == PermissionTypes.DELETE.value:
            has_permission = self._jv_can_delete(user)
        else:
            raise ValueError('Unknown permission type')
        
        if not has_permission:
            self._raise_permission_error(permission_type)
        
        return True
    
    def _raise_permission_error(self, permission_type):
        raise PermissionError(f'You do not have {permission_type} permission for this object')
    
    def _jv_can_create(self, user):
        return True
    
    def _jv_can_edit(self, user):
        return self._jv_can_create(user)
    
    def _jv_can_delete(self, user):
        return self._jv_can_create(user)
