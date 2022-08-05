from functools import reduce

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.user import UserView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import ContentItem
from jvapp.models.employer import *
from jvapp.models.employer import EmployerAuthGroup
from jvapp.models.user import JobVyneUser, UserEmployerPermissionGroup
from jvapp.permissions.employer import IsAdminOrEmployerOrReadOnlyPermission, IsAdminOrEmployerPermission
from jvapp.serializers.employer import get_serialized_auth_group, get_serialized_employer, get_serialized_employer_file, \
    get_serialized_employer_file_tag, get_serialized_employer_job, get_serialized_employer_page
from jvapp.utils.data import AttributeCfg, set_object_attributes

__all__ = ('EmployerView', 'EmployerJobView', 'EmployerAuthGroupView', 'EmployerUserView', 'EmployerUserActivateView')

from jvapp.utils.email import get_domain_from_email

from jvapp.utils.sanitize import sanitizer


BATCH_UPDATE_SIZE = 100


class EmployerView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_id=None):
        if employer_id:
            employer_id = int(employer_id)
            employer = self.get_employers(employer_id=employer_id)
            data = get_serialized_employer(
                employer,
                is_include_employees=(not isinstance(self.user, AnonymousUser)) and (
                    self.user.is_admin
                    or (self.user.employer_id == employer_id and self.user.is_employer)
                )
            )
        else:
            employers = self.get_employers(employer_filter=Q())
            data = [get_serialized_employer(e) for e in employers]
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @atomic
    def put(self, request, employer_id):
        employer = self.get_employers(employer_id=employer_id)
        if logo := self.files.get('logo'):
            employer.logo = logo[0]
        
        set_object_attributes(
            employer,
            self.data,
            {
                'email_domains': None,
                'color_primary': AttributeCfg(is_protect_existing=True),
                'color_secondary': AttributeCfg(is_protect_existing=True),
                'color_accent': AttributeCfg(is_protect_existing=True),
            }
        )
        
        employer.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        employer.save()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Updated employer data'
        })
    
    @staticmethod
    def get_employers(employer_id=None, employer_filter=None):
        if employer_id:
            employer_filter = Q(id=employer_id)
        
        employers = Employer.objects \
            .select_related('employer_size') \
            .prefetch_related(
                'employee',
                'employee__employer_permission_group',
                'employee__employer_permission_group__permission_group',
                'employee__employer_permission_group__permission_group__permissions'
            ) \
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
        user, is_new = UserView.get_or_create_user(self.data)
        employer_id = self.data['employer_id']
        if not user.employer_id:
            user.employer_id = employer_id
            user.save()
        elif user.employer_id != employer_id:
            return Response('This user already exists and is associated with a different employer')
        
        new_user_groups = []
        for group_id in self.data['permission_group_ids']:
            new_user_groups.append(
                UserEmployerPermissionGroup(
                    user=user,
                    employer_id=employer_id,
                    permission_group_id=group_id,
                    is_employer_approved=True
                )
            )
        UserEmployerPermissionGroup.objects.bulk_create(new_user_groups)
        
        user_full_name = f'{user.first_name} {user.last_name}'
        success_message = f'Account created for {user_full_name}' if is_new else f'Account already exists for {user_full_name}. Permissions were updated.'
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: success_message
        })
    
    @atomic
    def put(self, request):
        users = UserView.get_user(user_filter=Q(id__in=self.data['user_ids']))
        batchCount = 0
        while batchCount < len(users):
            user_employer_permissions_to_delete_filters = []
            user_employer_permissions_to_add = []
            for user in users[batchCount:batchCount + BATCH_UPDATE_SIZE]:
                set_object_attributes(user, self.data, {
                    'first_name': None,
                    'last_name': None
                })
                user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
                
                if permission_group_ids := self.data.get('permission_group_ids'):
                    user_employer_permissions_to_delete_filters.append(Q(user_id=user.id) & Q(employer_id=self.data['employer_id']))
                    for group_id in permission_group_ids:
                        user_employer_permissions_to_add.append(UserEmployerPermissionGroup(
                            user=user,
                            employer_id=self.data['employer_id'],
                            permission_group_id=group_id,
                            is_employer_approved=True
                        ))
                
                if add_permission_group_ids := self.data.get('add_permission_group_ids'):
                    for group_id in add_permission_group_ids:
                        user_employer_permissions_to_add.append(UserEmployerPermissionGroup(
                            user=user,
                            employer_id=self.data['employer_id'],
                            permission_group_id=group_id,
                            is_employer_approved=True
                        ))
                
                if remove_permission_group_ids := self.data.get('remove_permission_group_ids'):
                    for group_id in remove_permission_group_ids:
                        user_employer_permissions_to_delete_filters.append(Q(user_id=user.id) & Q(permission_group_id=group_id))
            
            JobVyneUser.objects.bulk_update(users, ['first_name', 'last_name'])
            if user_employer_permissions_to_delete_filters:
                def reduceFilters(allFilters, filter):
                    allFilters |= filter
                    return allFilters
                delete_filter = reduce(reduceFilters, user_employer_permissions_to_delete_filters)
                UserEmployerPermissionGroup.objects.filter(delete_filter).delete()
            UserEmployerPermissionGroup.objects.bulk_create(user_employer_permissions_to_add)
            batchCount += BATCH_UPDATE_SIZE
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
    
    
class EmployerFileView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        files = self.get_employer_files(employer_id=employer_id)
        return Response(status=status.HTTP_200_OK, data=[get_serialized_employer_file(f) for f in files])
    
    @atomic
    def post(self, request):
        if not self.data['employer_id']:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer_file = EmployerFile()
        file = self.files['file'][0] if self.files.get('file') else None
        self.update_employer_file(employer_file, self.data, self.user, file=file)
        return Response(status=status.HTTP_200_OK, data={
            'id': employer_file.id,
            SUCCESS_MESSAGE_KEY: f'Created a new file titled {employer_file.title}'
        })
        
    @atomic
    def put(self, request, file_id):
        if not self.data['employer_id']:
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer_file = self.get_employer_files(file_id=file_id)
        self.update_employer_file(employer_file, self.data, self.user)
        return Response(status=status.HTTP_200_OK, data={
            'id': employer_file.id,
            SUCCESS_MESSAGE_KEY: f'Updated file titled {employer_file.title}'
        })

    @staticmethod
    @atomic
    def update_employer_file(employer_file, data, user, file=None):
        set_object_attributes(employer_file, data, {
            'employer_id': None,
            'title': None
        })
        
        if file:
            employer_file.file = file

        employer_file.title = (
            employer_file.title
            or getattr(file, 'name', None)
            or employer_file.file.name.split('/')[-1]
        )
        
        permission_type = PermissionTypes.EDIT.value if employer_file.id else PermissionTypes.CREATE.value
        employer_file.jv_check_permission(permission_type, user)
        employer_file.save()
        
        employer_file.tags.clear()
        for tag in data.get('tags') or []:
            if isinstance(tag, str):
                tag = EmployerFileTagView.get_or_create_tag(tag, data['employer_id'])
                employer_file.tags.add(tag)
            else:
                employer_file.tags.add(tag['id'])
        
    @staticmethod
    def get_employer_files(file_id=None, employer_id=None, file_filter=None):
        file_filter = file_filter or Q()
        if file_id:
            file_filter &= Q(id=file_id)
        if employer_id:
            file_filter &= Q(employer_id=employer_id)

        files = EmployerFile.objects.prefetch_related('tags').filter(file_filter)
        if file_id:
            if not files:
                raise EmployerFile.DoesNotExist
            return files[0]
        
        return files


class EmployerFileTagView(JobVyneAPIView):
    
    def get(self, request):
        if not (employer_id := self.query_params['employer_id']):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        tags = self.get_employer_file_tags(employer_id)
        return Response(status=status.HTTP_200_OK, data=[get_serialized_employer_file_tag(t) for t in tags])
    
    @atomic
    def delete(self, request, tag_id):
        tag = EmployerFileTag.objects.get(id=tag_id)
        tag.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        tag.delete()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{tag.name} tag was deleted'
        })

    @staticmethod
    @atomic
    def get_or_create_tag(tag_name, employer_id):
        try:
            return EmployerFileTag.objects.get(name=tag_name, employer_id=employer_id)
        except EmployerFileTag.DoesNotExist:
            tag = EmployerFileTag(name=tag_name, employer_id=employer_id)
            tag.save()
            return tag

    @staticmethod
    def get_employer_file_tags(employer_id):
        return EmployerFileTag.objects.filter(employer_id=employer_id)
    
    
class EmployerPageView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerOrReadOnlyPermission]

    def get(self, request):
        if not (employer_id := self.query_params['employer_id']):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer_page = self.get_employer_page(employer_id)
        return Response(
            status=status.HTTP_200_OK,
            data=get_serialized_employer_page(employer_page) if employer_page else None
        )
    
    @atomic
    def put(self, request):
        if not (employer_id := self.data['employer_id']):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer_page = self.get_employer_page(employer_id)
        if employer_page:
            current_sections = {ci.id: ci for ci in employer_page.content_item.all()}
        else:
            employer_page = EmployerPage(employer_id=employer_id)
            current_sections = {}
        employer_page.is_viewable = self.data['is_viewable']
        employer_page.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        employer_page.save()
        
        sections = self.data['sections']
        for sectionIdx, sectionData in enumerate(sections):
            section = None
            if sectionId := sectionData.get('id'):
                # Remove the section from the dict so we know it has been used
                section = current_sections.pop(sectionId, None)
            if not section:
                section = ContentItem(type=sectionData['type'])
            section.orderIdx = sectionIdx
            section.header = sectionData['header']
            section.config = sectionData.get('config')
            item_parts = sectionData['item_parts']
            for part in item_parts:
                if html_content := part.get('html_content'):
                    part['html_content'] = sanitizer.clean(html_content)
            section.item_parts = item_parts
            section.save()
            employer_page.content_item.add(section)
        
        # Any sections still in the dict are not used and should be removed
        for content_item_id, content_item in current_sections.items():
            employer_page.content_item.remove(content_item_id)
            content_item.delete()
            
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Updated the profile page'
        })
        
    @staticmethod
    def get_employer_page(employer_id):
        try:
            return EmployerPage.objects.prefetch_related('content_item').get(employer_id=employer_id)
        except EmployerPage.DoesNotExist:
            return None


class EmployerFromDomainView(JobVyneAPIView):
    
    def get(self, request):
        if not (email := self.query_params.get('email')):
            return Response('An email address is required', status=status.HTTP_400_BAD_REQUEST)
        
        if not (email_domain := get_domain_from_email(email)):
            return Response(f'Could not parse email domain for {email}', status=status.HTTP_400_BAD_REQUEST)
        
        employers = {e.email_domains: e for e in Employer.objects.all()}
        matched_employers = []
        for domains, employer in employers.items():
            if not domains:
                continue
            if email_domain in domains:
                matched_employers.append({'id': employer.id, 'name': employer.employer_name})
        
        return Response(
            status=status.HTTP_200_OK,
            data=matched_employers
        )
