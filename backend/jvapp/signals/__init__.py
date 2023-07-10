__all__ = ('add_audit_fields', 'add_owner_fields', 'set_user_permission_groups_on_save')

import re

from django.core.files import File
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from jvapp.apis.job_seeker import ApplicationTemplateView
from jvapp.apis.job_subscription import JobSubscriptionView
from jvapp.apis.social import SocialLinkView
from jvapp.models.employer import Employer, EmployerAuthGroup, EmployerJobApplicationRequirement, is_default_auth_group
from jvapp.models.job_seeker import JobApplication, JobApplicationTemplate
from jvapp.models.social import SocialLink
from jvapp.models.tracking import PageView
from jvapp.models.user import JobVyneUser, UserEmployerPermissionGroup
from jvapp.utils.file import get_file_extension, get_file_name
from jvapp.utils.image import resize_image_with_fill


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


@receiver(pre_save, sender=JobVyneUser)
def prevent_duplicate_user(sender, instance, *args, **kwargs):
    new_user_emails = [instance.email]
    if instance.business_email:
        new_user_emails.append(instance.business_email)
    current_user_filter = Q(email__in=new_user_emails) | Q(business_email__in=new_user_emails)
    current_user_filter &= ~Q(id=instance.id)
    existing_users = JobVyneUser.objects.filter(current_user_filter)
    if existing_users:
        raise ValueError('A user with this email address already exists')

    
@receiver(post_save, sender=JobVyneUser)
def create_employee_referral_link(sender, instance, *args, **kwargs):
    if instance.employer_id:
        SocialLinkView.get_or_create_employee_referral_links([instance], instance.employer)

    
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
        
        
@receiver(post_save, sender=Employer)
def add_job_application_requirements(sender, instance, created, *args, **kwargs):
    # Only add requirements if this is a new employer
    if not created:
        return
    
    requirements = [
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='first_name', is_required=True, is_optional=False, is_hidden=False, is_locked=True
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='last_name', is_required=True, is_optional=False, is_hidden=False, is_locked=True
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='email', is_required=True, is_optional=False, is_hidden=False, is_locked=True
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='phone_number', is_required=False, is_optional=True, is_hidden=False, is_locked=False
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='linkedin_url', is_required=False, is_optional=True, is_hidden=False, is_locked=False
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='resume', is_required=True, is_optional=False, is_hidden=False, is_locked=False
        ),
        EmployerJobApplicationRequirement(
            created_dt=timezone.now(), modified_dt=timezone.now(),
            application_field='academic_transcript', is_required=False, is_optional=False, is_hidden=True, is_locked=False
        )
    ]
    for application_requirement in requirements:
        application_requirement.employer = instance
        
    EmployerJobApplicationRequirement.objects.bulk_create(requirements)


@receiver(post_save, sender=Employer)
def generate_logo_sizes(sender, instance, created, *args, **kwargs):
    if instance.logo and not instance.logo_square_88:
        new_image = resize_image_with_fill(instance.logo, 88, 88)
        if not new_image:
            return
        file_name = get_file_name(instance.logo.url, is_include_extension=False)
        file_extension = get_file_extension(instance.logo.url)
        instance.logo_square_88 = File(new_image, name=f'{file_name}_square_88.{file_extension}')
        instance.save()
        new_image.close()


@receiver(post_save, sender=Employer)
def create_employer_job_board(sender, instance, created, *args, **kwargs):
    if created:
        link = SocialLink(
            is_default=True, name='Main Job Board', employer_id=instance.id
        )
        link.save()
        # If this is an employer then, they should only be subscribed to their jobs
        if instance.organization_type & Employer.ORG_TYPE_EMPLOYER:
            employer_subscription = JobSubscriptionView.get_or_create_employer_subscription(instance.id)
            link.job_subscriptions.add(employer_subscription.id)


@receiver(post_save, sender=Employer)
def create_employer_key(sender, instance, created, *args, **kwargs):
    if created:
        instance.employer_key = re.sub('[^a-z0-9]', '-', instance.employer_name.lower())
        existing_employer_filter = Q(employer_key=instance.employer_key) & ~Q(id=instance.id)
        if Employer.objects.filter(existing_employer_filter):
            instance.employer_key = f'{instance.employer_key}{instance.id}'
        instance.save()
        
        
@receiver(pre_save, sender=JobApplication)
def parse_social_link(sender, instance, *args, **kwargs):
    if instance.social_link:
        instance.referrer_employer_id = instance.referrer_employer_id or instance.social_link.employer_id
        instance.referrer_user_id = instance.referrer_user_id or instance.social_link.owner_id
        
        
@receiver(pre_save, sender=PageView)
def parse_social_link(sender, instance, *args, **kwargs):
    if instance.social_link:
        instance.employer_id = instance.employer_id or instance.social_link.employer_id
        instance.page_owner_id = instance.page_owner_id or instance.social_link.owner_id
        