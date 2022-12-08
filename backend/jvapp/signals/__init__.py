from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.apis.job_seeker import ApplicationTemplateView
from jvapp.apis.social import SocialLinkFilterView
from jvapp.models import EmployerAuthGroup, JobApplication, JobApplicationTemplate, JobVyneUser, SocialLinkFilter, \
    UserEmployerPermissionGroup
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
    # Only set permission groups if the user is associated with an employer
    if not instance.employer_id:
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
                        permission_group_id=default_permission_group.id,
                        is_employer_approved=user_type_bit not in JobVyneUser.USER_TYPES_APPROVAL_REQUIRED
                    )
                )

    UserEmployerPermissionGroup.objects.bulk_create(groups_to_add, ignore_conflicts=True)
    

@receiver(post_save, sender=JobVyneUser)
def generate_primary_social_link(sender, instance, *args, **kwargs):
    # User must be associated with an employer to have a social link
    if not instance.employer_id:
        return
    
    try:
        # Check if primary link already exists
        SocialLinkFilter.objects.get(owner_id=instance.id, is_primary=True)
    except SocialLinkFilter.DoesNotExist:
        SocialLinkFilterView.create_or_update_link_filter(
            SocialLinkFilter(is_primary=True), {
                'owner_id': instance.id,
                'employer_id': instance.employer_id,
                'is_default': True
            }
        )

       
@receiver(post_save, sender=JobVyneUser)
def link_job_applications(sender, instance, *args, **kwargs):
    # User must have verified their email before we can show them completed job applications
    if not instance.is_email_verified:
        return
    
    orphaned_applications = JobApplication.objects.filter(email=instance.email, user__isnull=True)
    for app in orphaned_applications:
        app.user_id = instance.id
        
    JobApplication.objects.bulk_update(orphaned_applications, ['user_id'])
    
    # Create an application template for the user if they don't already have one
    if (not ApplicationTemplateView.get_application_template(instance.id)) and orphaned_applications:
        app_defaults = orphaned_applications[0]
        JobApplicationTemplate(
            owner=instance,
            first_name=app_defaults.first_name,
            last_name=app_defaults.last_name,
            email=app_defaults.email,
            phone_number=app_defaults.phone_number,
            linkedin_url=app_defaults.linkedin_url,
            resume=app_defaults.resume
        ).save()
    