# Generated by Django 4.0.5 on 2022-07-13 04:01

from django.db import migrations

from jvapp.models.employer import EmployerAuthGroup, EmployerPermission

GROUPS = (('Admin', 16), ('HR Professional', 16), ('Employee', 4), ('Influencer', 8))
PERMISSIONS = (
    ('Add admin users', '', ['Admin'], 16),
    ('Add employees', '', ['Admin', 'HR Professional'], 16),
    ('Change admin user permissions', '', ['Admin'], 16),
    ('Change employee permissions', 'Covers all users except admin users.', ['Admin', 'HR Professional'], 16),
    ('Manage custom permission groups', 'Allows the user to create, edit, and delete custom permission groups.',
     ['Admin'], 16),
    ('Manage employer content',
     'Allows the user to create, edit, and delete employer content such as the employer description.',
     ['Admin', 'HR Professional'], 16),
    ('Manage employer jobs',
     'Allows the user to create, edit, and delete. For most employers, most job data will automatically be pulled from your ATS.',
     ['Admin', 'HR Professional'], 16),
    ('Manage employee referral bonuses',
     'Allows user to set and modify the referral bonus for any job or groups of jobs.', ['Admin', 'HR Professional'], 16),
    ('Add personal employee content',
     'Allows employees to add text and video content about their job which is displayed for any of their unique job links.',
     ['Employee'], 4),
    ('Manage billing settings', 'Allows user to update billing details and set budget limits', ['Admin'], 16)
)


def add_permissions(apps, schema_editor):
    auth_groups = {}
    for name, user_type_bit in GROUPS:
        new_group = EmployerAuthGroup(name=name, is_default=1, user_type_bit=user_type_bit)
        new_group.save()
        auth_groups[name] = new_group
    
    for name, description, group_names in PERMISSIONS:
        new_permission = EmployerPermission(name=name, description=description)
        new_permission.save()
        
        for group_name in group_names:
            auth_groups[group_name].permissions.add(new_permission)


class Migration(migrations.Migration):
    dependencies = [
        ('jvapp', '0008_employerauthgroup_employer_and_more'),
    ]
    
    operations = [
        migrations.RunPython(add_permissions, atomic=True),
    ]
