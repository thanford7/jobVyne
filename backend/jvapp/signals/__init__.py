import functools

from django.db.models import Q
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.models import EmployerAuthGroup, JobVyneUser

__all__ = ('add_audit_fields', 'update_user_types_on_group_save', 'update_user_types_on_group_delete')


def _reduce_user_type_bits(permission_groups):
    return functools.reduce(
        lambda user_type_bits, group: group.user_type_bit | user_type_bits,
        permission_groups
    )


def _update_user_types_on_group_change(instance):
    impacted_users = JobVyneUser.objects \
        .prefetch_related('permission_groups') \
        .filter(permission_groups__in=[instance])
    
    for user in impacted_users:
        user.user_type_bits = _reduce_user_type_bits(user.permission_groups.all())
    
    JobVyneUser.objects.bulk_update(impacted_users, ['user_type_bits'])


@receiver(pre_save)
def add_audit_fields(sender, instance, *args, **kwargs):
    if hasattr(instance, 'created_dt') and not instance.created_dt:
        instance.created_dt = timezone.now()
    
    if hasattr(instance, 'modified_dt'):
        instance.modified_dt = timezone.now()


@receiver(post_save, sender=EmployerAuthGroup)
def update_user_types_on_group_save(sender, instance, *args, **kwargs):
    _update_user_types_on_group_change(instance)


@receiver(post_delete, sender=EmployerAuthGroup)
def update_user_types_on_group_delete(sender, instance, *args, **kwargs):
    _update_user_types_on_group_change(instance)
    
    
@receiver(m2m_changed, sender=JobVyneUser.permission_groups.through)
def update_user_types_on_user_permission_change(sender, instance, action, *args, **kwargs):
    if not isinstance(instance, JobVyneUser):
        return
    
    if action not in ('post_add', 'post_remove', 'post_clear'):
        return

    instance.user_type_bits = _reduce_user_type_bits(instance.permission_groups.all())
    
    
