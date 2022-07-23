from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.user import UserView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.employer import *
from jvapp.models.employer import EmployerAuthGroup
from jvapp.models.user import JobVyneUser, USER_MANAGEMENT_PERMISSIONS
from jvapp.permissions.employer import IsAdminOrEmployerOrReadOnlyPermission, IsAdminOrEmployerPermission
from jvapp.serializers.employer import get_serialized_auth_group, get_serialized_employer, get_serialized_employer_job
from jvapp.utils.data import set_object_attributes

__all__ = ('EmployerView', 'EmployerJobView', 'EmployerAuthGroupView', 'EmployerUserView', 'EmployerUserActivateView')


class EmployerView(JobVyneAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_id=None):
        if employer_id:
            employer_id = int(employer_id)
            employer = self.get_employers(employer_id=employer_id)
            can_view_users = self.user.has_employer_permission(USER_MANAGEMENT_PERMISSIONS, is_all_true=False)
            data = get_serialized_employer(
                employer,
                is_include_employees=(self.user.is_admin or self.user.employer_id == employer_id)
            )
        else:
            employers = self.get_employers(employer_filter=Q())
            data = [get_serialized_employer(e) for e in employers]
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_employers(employer_id=None, employer_filter=None):
        if employer_id:
            employer_filter = Q(id=employer_id)
        
        employers = Employer.objects \
            .select_related('employerSize') \
            .prefetch_related('employee', 'employee__permission_groups') \
            .filter(employer_filter)
        
        if employer_id:
            if not employers:
                raise Employer.DoesNotExist
            return employers[0]
        
        return employers


class EmployerJobView(JobVyneAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_job_id=None):
        if employer_job_id:
            job = self.get_employer_jobs(employer_job_id=employer_job_id)
            data = get_serialized_employer_job(job)
        elif employer_id := self.query_params.get('employer_id'):
            employer_id = employer_id[0]
            job_filter = Q(employer_id=employer_id)
            jobs = self.get_employer_jobs(employer_job_filter=job_filter)
            data = [get_serialized_employer_job(j) for j in jobs]
        else:
            return Response('A job ID or employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @staticmethod
    def get_employer_jobs(employer_job_id=None, employer_job_filter=None):
        if employer_job_id:
            employer_job_filter = Q(id=employer_job_id)
        
        jobs = EmployerJob.objects \
            .select_related(
            'jobDepartment',
            'state',
            'country'
        ) \
            .filter(employer_job_filter)
        
        if employer_job_id:
            if not jobs:
                raise EmployerJob.DoesNotExist
            return jobs[0]
        
        return jobs


class EmployerAuthGroupView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def get(self, request):
        auth_groups = self.get_auth_groups(employer_id=self.user.employer_id)
        all_permissions = EmployerPermission.objects.all()
        return Response(
            status=status.HTTP_200_OK,
            data=[get_serialized_auth_group(ag, all_permissions, auth_groups, self.user) for ag in auth_groups]
        )
    
    @atomic
    def post(self, request):
        auth_group = EmployerAuthGroup(
            name=self.data['name'],
            user_type_bit=self.data['user_type_bit'],
            employer_id=self.data['employer_id']
        )
        auth_group.jv_check_permission(PermissionTypes.CREATE.value, self.user)
        auth_group.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                'auth_group_id': auth_group.id,
                SUCCESS_MESSAGE_KEY: f'{auth_group.name} group saved'
            }
        )
    
    @atomic
    def put(self, request, auth_group_id):
        auth_group = EmployerAuthGroup.objects.get(id=auth_group_id)
        set_object_attributes(auth_group, self.data, {
            'name': None,
            'user_type_bit': None,
            'is_default': None
        })
        auth_group.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        auth_group.save()
        
        if permissions := self.data.get('permissions'):
            auth_group.jv_check_can_update_permissions(self.user)
            auth_group.permissions.clear()
            for permission in permissions:
                if permission['is_permitted']:
                    auth_group.permissions.add(permission['id'])
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{auth_group.name} group saved'
        })
    
    @atomic
    def delete(self, request, auth_group_id):
        auth_group = EmployerAuthGroup.objects.get(id=auth_group_id)
        auth_group.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        auth_group.delete()

        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{auth_group.name} group deleted'
        })
    
    @staticmethod
    def get_auth_groups(auth_group_filter=None, employer_id=None):
        auth_group_filter = auth_group_filter or Q()
        if employer_id:
            auth_group_filter &= (Q(employer_id=employer_id) | Q(employer_id__isnull=True))
        return EmployerAuthGroup.objects.prefetch_related('permissions').filter(auth_group_filter)


class EmployerUserView(JobVyneAPIView):
    
    @atomic
    def post(self, request):
        user = JobVyneUser.objects.create_user(
            self.data['email'],
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            employer_id=self.data['employer_id'],
            user_type_bits=-1  # This is just a placeholder. The actual value is derived from the permission groups
        )
        
        for group_id in self.data['permission_group_ids']:
            user.permission_groups.add(group_id)
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Account created for {user.first_name} {user.last_name}'
        })
    
    @atomic
    def put(self, request):
        users = UserView.get_user(user_filter=Q(id__in=self.data['user_ids']))
        for user in users:
            set_object_attributes(user, self.data, {
                'first_name': None,
                'last_name': None
            })
            user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
            
            # TODO: See if there is a way to do this in one database call (not per user)
            if permission_group_ids := self.data.get('permission_group_ids'):
                user.permission_groups.clear()
                for group_id in permission_group_ids:
                    user.permission_groups.add(group_id)
            
            if add_permission_group_ids := self.data.get('add_permission_group_ids'):
                for group_id in add_permission_group_ids:
                    user.permission_groups.add(group_id)
            
            if remove_permission_group_ids := self.data.get('remove_permission_group_ids'):
                for group_id in remove_permission_group_ids:
                    user.permission_groups.remove(group_id)
        
        JobVyneUser.objects.bulk_update(users, ['first_name', 'last_name'])
        userCount = len(users)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{userCount} {"user" if userCount == 1 else "users"} updated'
        })


class EmployerUserActivateView(JobVyneAPIView):
    
    @atomic
    def put(self, request):
        is_deactivate = self.data['is_deactivate']
        users = UserView.get_user(user_filter=Q(id__in=self.data['user_ids']))
        for user in users:
            user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
            user.is_employer_deactivated = is_deactivate
        
        JobVyneUser.objects.bulk_update(users, ['is_employer_deactivated'])
        userCount = len(users)
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{userCount} {"user" if userCount == 1 else "users"} {"deactivated" if is_deactivate else "activated"}'
        })
