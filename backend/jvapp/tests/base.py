import names
from django.test import TestCase
from rest_framework.test import APIClient

from jvapp.models import *
from jvapp.models.user import StandardPermissionGroups
from jvapp.urls import api_path


class BaseTestCase(TestCase):
    REQUEST_GET = 'GET'
    REQUEST_POST = 'POST'
    REQUEST_PUT = 'PUT'
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.employer_permission_groups = {g.name: g for g in EmployerAuthGroup.objects.all()}
        self.permissions = {p.name: p for p in EmployerPermission.objects.all()}
        self.employer = self.create_employer('ChickFilet')
        self.user_admin = self.create_user(
            JobVyneUser.USER_TYPE_ADMIN, first_name='Billy', last_name='Jean'
        )
        self.user_employer_admin = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYER, first_name='Britney', last_name='Spears',
            employer_id=self.employer.id, auth_group_names=[StandardPermissionGroups.ADMIN.value]
        )
        self.user_employer_hr = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYER, first_name='Scooby', last_name='Doo',
            employer_id=self.employer.id, auth_group_names=[StandardPermissionGroups.HR.value]
        )
        self.user_employee = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYEE, first_name='Shark', last_name='Nado', employer_id=self.employer.id
        )
    
    def make_request(self, url, request_type, data=None):
        url = f'/{api_path}{url}'
        
        if request_type == self.REQUEST_GET:
            return self.client.get(url, data)
        elif request_type == self.REQUEST_POST:
            return self.client.post(url, data=data)
        elif request_type == self.REQUEST_PUT:
            return self.client.put(url, data=data)
    
    def create_employer(self, name):
        employer = Employer(employer_name=name)
        employer.save()
        return employer
    
    def create_employer_auth_group(self, name, user_type_bit, employer_id=None, is_default=False, permissions=None):
        employer_auth_group = EmployerAuthGroup(
            name=name,
            user_type_bit=user_type_bit,
            employer_id=employer_id,
            is_default=is_default
        )
        employer_auth_group.save()
        
        permissions = permissions or []
        for permission in permissions:
            employer_auth_group.permissions.add(permission)
        
        return employer_auth_group
    
    def create_user(self, user_type_bits, email=None, first_name=None, last_name=None, employer_id=None,
                    auth_group_names=None):
        first_name = first_name or names.get_first_name()
        last_name = last_name or names.get_full_name()
        email = email or f'{first_name}_{last_name}@jobvyne.com'
        user = JobVyneUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            employer_id=employer_id,
            user_type_bits=user_type_bits
        )
        
        user.save()
        auth_group_names = auth_group_names or []
        for group_name in auth_group_names:
            auth_group = self.employer_permission_groups[group_name]
            UserEmployerPermissionGroup(
                user=user,
                employer_id=employer_id,
                permission_group=auth_group,
                is_employer_approved=True
            ).save()
        
        return user
