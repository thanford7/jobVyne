from dataclasses import dataclass

from django.db.models import Q

from jvapp.models.user import StandardPermissionGroups


@dataclass
class Group:
    name: str  # See StandardPermissionGroups
    user_type_bit: int
    is_default: bool
    
    
@dataclass
class Permission:
    name: str
    description: str
    group_names: tuple  # See StandardPermissionGroups
    user_type_bit: int
    

# Note don't add a default for job seeker groups (bit 2) - must be added manually be the employer
groups_cfg = (
    Group(name=StandardPermissionGroups.ADMIN.value, user_type_bit=16, is_default=False),
    Group(name=StandardPermissionGroups.HR.value, user_type_bit=16, is_default=True),
    Group(name=StandardPermissionGroups.EMPLOYEE.value, user_type_bit=4, is_default=True),
    Group(name=StandardPermissionGroups.INFLUENCER.value, user_type_bit=8, is_default=True),
    Group(name=StandardPermissionGroups.JOB_SEEKER.value, user_type_bit=2, is_default=False),
)

permissions_cfg = (
    Permission(
        name='Manage users',
        description='Allows the user to create and edit new users.',
        group_names=(StandardPermissionGroups.ADMIN.value,),
        user_type_bit=16
    ),
    Permission(
        name='Change user permissions',
        description='',
        group_names=(StandardPermissionGroups.ADMIN.value,),
        user_type_bit=16
    ),
    Permission(
        name='Manage custom permission groups',
        description='Allows the user to create, edit, and delete custom permission groups.',
        group_names=(StandardPermissionGroups.ADMIN.value,),
        user_type_bit=16
    ),
    Permission(
        name='Manage employer content',
        description='Allows the user to create, edit, and delete employer content such as the employer description.',
        group_names=(StandardPermissionGroups.ADMIN.value, StandardPermissionGroups.HR.value),
        user_type_bit=16
    ),
    Permission(
        name='Manage employer jobs',
        description='Allows the user to create, edit, and delete. For most employers, most job data will automatically be pulled from your ATS.',
        group_names=(StandardPermissionGroups.ADMIN.value, StandardPermissionGroups.HR.value),
        user_type_bit=16
    ),
    Permission(
        name='Manage employee referral bonuses',
        description='Allows user to set and modify the referral bonus for any job or groups of jobs.',
        group_names=(StandardPermissionGroups.ADMIN.value, StandardPermissionGroups.HR.value),
        user_type_bit=16
    ),
    Permission(
        name='Add personal employee content',
        description='Allows employees to add text and video content about their job which is displayed for any of their unique job links.',
        group_names=(StandardPermissionGroups.EMPLOYEE.value,),
        user_type_bit=4
    ),
    Permission(
        name='Manage billing settings',
        description='Allows user to update billing details and set budget limits.',
        group_names=(StandardPermissionGroups.ADMIN.value,),
        user_type_bit=16
    ),
    Permission(
        name='Manage employer settings',
        description='Allows user to update employer settings.',
        group_names=(StandardPermissionGroups.ADMIN.value,),
        user_type_bit=16
    ),
)


def update_permissions(apps, schema_editor):
    EmployerAuthGroup = apps.get_model('jvapp', 'EmployerAuthGroup')
    EmployerPermission = apps.get_model('jvapp', 'EmployerPermission')
    
    auth_groups = {
        ag.name: ag for ag in
        EmployerAuthGroup.objects.filter(employer_id=None)
    }
    used_auth_group_names = []
    
    # Add / update groups
    for group_cfg in groups_cfg:
        if not (group := auth_groups.get(group_cfg.name)):
            group = EmployerAuthGroup(name=group_cfg.name)
        group.is_default = group_cfg.is_default
        group.user_type_bit = group_cfg.user_type_bit
        group.save()
        auth_groups[group.name] = group
        used_auth_group_names.append(group.name)
        
        # Remove permissions - they will be refreshed further down in this code
        group.permissions.clear()
    
    # Delete any groups that are no longer present
    EmployerAuthGroup.objects.filter(employer_id=None).filter(~Q(name__in=used_auth_group_names)).delete()
    for group_name in auth_groups.keys():
        if group_name not in used_auth_group_names:
            del auth_groups[group_name]

    permissions = {ep.name: ep for ep in EmployerPermission.objects.all()}
    used_permission_names = []
    # Add / update permissions
    for permission_cfg in permissions_cfg:
        if not (permission := permissions.get(permission_cfg.name)):
            permission = EmployerPermission(name=permission_cfg.name)
        permission.description = permission_cfg.description
        permission.user_type_bits = permission_cfg.user_type_bit
        permission.save()
        used_permission_names.append(permission.name)
        
        for group_name in permission_cfg.group_names:
            auth_groups[group_name].permissions.add(permission)

    # Delete any permissions that are no longer present
    EmployerPermission.objects.filter(~Q(name__in=used_permission_names)).delete()
