import functools

from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.models import EmployerAuthGroup, JobVyneUser
from jvapp.models.employer import is_default_auth_group

__all__ = ('add_audit_fields', 'update_user_types_on_group_save', 'update_user_types_on_group_delete')


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
    

def _reduce_user_type_bits(permission_groups):
    return functools.reduce(
        lambda user_type_bits, group: group.user_type_bit | user_type_bits,
        permission_groups, 0
    )


def _update_user_types_on_group_change(instance, is_delete):
    impacted_users = JobVyneUser.objects \
        .prefetch_related('permission_groups') \
        .filter(permission_groups__in=[instance])

    cache_default_user_groups = {}
    filter_fn = lambda group: (not is_delete) or group.id != instance.id
    for user in impacted_users:
        if not (default_user_groups := cache_default_user_groups.get(user.employer_id)):
            default_user_groups = _get_default_user_groups(user.employer_id)
            cache_default_user_groups[user.employer_id] = default_user_groups
        new_user_type_bits = _reduce_user_type_bits((g for g in user.permission_groups.all() if filter_fn(g)))
        
        # Add the default group for any user type bits that would be lost
        lost_user_type_bits = (new_user_type_bits ^ user.user_type_bits) & user.user_type_bits
        for user_type_bit in JobVyneUser.ALL_USER_TYPES:
            if user_type_bit & lost_user_type_bits:
                user.permission_groups.add(default_user_groups[user_type_bit])
        
        user.user_type_bits |= new_user_type_bits
    
    JobVyneUser.objects.bulk_update(impacted_users, ['user_type_bits'])


@receiver(pre_save)
def add_audit_fields(sender, instance, *args, **kwargs):
    if hasattr(instance, 'created_dt') and not instance.created_dt:
        instance.created_dt = timezone.now()
    
    if hasattr(instance, 'modified_dt'):
        instance.modified_dt = timezone.now()


@receiver(post_save, sender=EmployerAuthGroup)
def update_user_types_on_group_save(sender, instance, *args, **kwargs):
    _update_user_types_on_group_change(instance, False)


@receiver(pre_delete, sender=EmployerAuthGroup)
def update_user_types_on_group_delete(sender, instance, *args, **kwargs):
    _update_user_types_on_group_change(instance, True)
    
    
@receiver(m2m_changed, sender=JobVyneUser.permission_groups.through)
def update_user_types_on_user_permission_change(sender, instance, action, *args, **kwargs):
    if not isinstance(instance, JobVyneUser):
        return
    
    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    instance.user_type_bits = _reduce_user_type_bits(instance.permission_groups.all())
    instance.save()
    
    
@receiver(post_save, sender=JobVyneUser)
def set_user_permission_groups_on_save(sender, instance, *args, **kwargs):
    if len(instance.permission_groups.all()):
        return
    
    default_permission_groups = _get_default_user_groups(instance.employer_id)
    for user_type_bit in JobVyneUser.ALL_USER_TYPES:
        if instance.user_type_bits & user_type_bit:
            default_permission_group = default_permission_groups.get(user_type_bit)
            if default_permission_group:
                instance.permission_groups.add(default_permission_group)
