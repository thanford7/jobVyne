from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.models import EmployerAuthGroup, JobVyneUser, UserEmployerPermissionGroup
from jvapp.models.employer import is_default_auth_group

__all__ = ('add_audit_fields', 'add_owner_fields', 'set_user_permission_groups_on_save')


def _get_default_user_groups(employer_id):
    # Get the default permission groups for each user type
    group_filter = (
            Q(is_default=True)
            & (Q(employer_id__isnull=True) | Q(employer_id=employer_id))
    )
    
    default_permission_groups = EmployerAuthGroup.objects.filter(group_filter)

    default_permission_group_dict = {}
    for user_type_bit in JobVyneUser.ALL_USER_TYPES:
        default_permission_group_dict[user_type_bit] = next(
            (
                g for g in default_permission_groups
                if g.user_type_bit & user_type_bit and is_default_auth_group(g, default_permission_groups)
            ),
            None
        )
    return default_permission_group_dict


@receiver(pre_save)
def add_audit_fields(sender, instance, *args, **kwargs):
    if hasattr(instance, 'created_dt') and not instance.created_dt:
        instance.created_dt = timezone.now()
    
    if hasattr(instance, 'modified_dt'):
        instance.modified_dt = timezone.now()


@receiver(pre_save)
def add_owner_fields(sender, instance, *args, **kwargs):
    if hasattr(instance, 'created_user') and not instance.id:
        instance.created_dt = timezone.now()
    
    if hasattr(instance, 'modified_user'):
        instance.modified_dt = timezone.now()
    
    
@receiver(post_save, sender=JobVyneUser)
def set_user_permission_groups_on_save(sender, instance, *args, **kwargs):
    # Only set permission groups if the user doesn't already have any
    if len(instance.permission_groups.all()):
        return
    
    default_permission_groups = _get_default_user_groups(instance.employer_id)
    groups_to_add = []
    for user_type_bit in JobVyneUser.ALL_USER_TYPES:
        if instance.user_type_bits and (instance.user_type_bits & user_type_bit):
            default_permission_group = default_permission_groups.get(user_type_bit)
            if default_permission_group:
                groups_to_add.append(
                    UserEmployerPermissionGroup(
                        user_id=instance.id,
                        employer_id=instance.employer_id,
                        permission_group_id=default_permission_group.id
                    )
                )

    UserEmployerPermissionGroup.objects.bulk_create(groups_to_add)
