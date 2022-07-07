from enum import Enum

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.utils.logger import getLogger

__all__ = ('AuditFields', 'JobVynePermissionsMixin')


logger = getLogger()


@receiver(pre_save)
def add_audit_fields(sender, instance, *args, **kwargs):
    if hasattr(instance, 'created_dt') and not instance.created_dt:
        instance.created_dt = timezone.now()
    
    if hasattr(instance, 'modified_dt'):
        instance.modified_dt = timezone.now()


class AuditFields(models.Model):
    created_dt = models.DateTimeField()
    modified_dt = models.DateTimeField()

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
            raise PermissionError(f'You do not have {permission_type} permission for this object')
        
        return True
    
    def _jv_can_create(self, user):
        return True
    
    def _jv_can_edit(self, user):
        return self._jv_can_create(user)
    
    def _jv_can_delete(self, user):
        return self._jv_can_create(user)
