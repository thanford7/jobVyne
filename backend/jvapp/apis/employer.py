from functools import reduce

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.user import UserView
from jvapp.models.abstract import PermissionTypes
from jvapp.models.content import ContentItem
from jvapp.models.employer import *
from jvapp.models.employer import EmployerAuthGroup, EmployerReferralBonusRule
from jvapp.models.user import JobVyneUser, PermissionName, UserEmployerPermissionGroup
from jvapp.permissions.employer import IsAdminOrEmployerOrReadOnlyPermission, IsAdminOrEmployerPermission
from jvapp.serializers.employer import get_serialized_auth_group, get_serialized_employer, \
    get_serialized_employer_bonus_rule, get_serialized_employer_file, \
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
            .select_related('employer_size', 'default_bonus_currency') \
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
    permission_classes = [IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request, employer_job_id=None):
        if employer_job_id:
            job = self.get_employer_jobs(employer_job_id=employer_job_id)
            rules = EmployerBonusRuleView.get_employer_bonus_rules(self.user, employer_id=job.employer_id)
            data = get_serialized_employer_job(job, rules=rules)
        elif employer_id := self.query_params.get('employer_id'):
            employer_id = employer_id[0]
            job_filter = Q(employer_id=employer_id)
            jobs = self.get_employer_jobs(employer_job_filter=job_filter)
            rules = EmployerBonusRuleView.get_employer_bonus_rules(self.user, employer_id=employer_id)
            data = [get_serialized_employer_job(j, rules) for j in jobs]
        else:
            return Response('A job ID or employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def put(self, request):
        jobs = EmployerJob.objects.filter(id__in=self.data['job_ids'])
        jobs_to_update = []
        for job in jobs:
            job.referral_bonus = self.data['referral_bonus']
            job.referral_bonus_currency_id = self.data['referral_bonus_currency']['name']
            jobs_to_update.append(job)
        
        EmployerJob.objects.bulk_update(jobs_to_update, ['referral_bonus', 'referral_bonus_currency_id'], batch_size=1000)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Updated referral bonus for {len(jobs)} {"jobs" if len(jobs) > 1 else "job"}'
        })
    
    @staticmethod
    def get_employer_jobs(employer_job_id=None, employer_job_filter=None):
        if employer_job_id:
            employer_job_filter = Q(id=employer_job_id)
        
        jobs = EmployerJob.objects\
            .select_related('job_department', 'employer', 'referral_bonus_currency')\
            .prefetch_related(
                'locations',
                'locations__city',
                'locations__state',
                'locations__country'
            )\
            .filter(employer_job_filter)
        
        if employer_job_id:
            if not jobs:
                raise EmployerJob.DoesNotExist
            return jobs[0]
        
        return jobs
    
    
class EmployerBonusDefaultView(JobVyneAPIView):
    
    @atomic
    def put(self, request):
        if not (employer_id := self.data.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        employer = EmployerView.get_employers(employer_id=employer_id)
        
        employer.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        self.user.has_employer_permission(PermissionName.MANAGE_REFERRAL_BONUSES.value, self.user.employer_id)
        
        self.data['default_bonus_currency_id'] = self.data['default_bonus_currency']['name']
        set_object_attributes(employer, self.data, {
            'default_bonus_amount': None,
            'default_bonus_currency_id': None,
        })
        employer.save()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Bonus rule defaults updated'
        })
        
    
class EmployerBonusRuleView(JobVyneAPIView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        rules = self.get_employer_bonus_rules(self.user, employer_id=employer_id)
        return Response(
            status=status.HTTP_200_OK,
            data=[get_serialized_employer_bonus_rule(rule) for rule in rules]
        )
    
    @atomic
    def post(self, request):
        rule = EmployerReferralBonusRule(employer_id=self.data['employer_id'])
        self.update_bonus_rule(self.user, rule, self.data)
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: 'Referral bonus rule added'
            }
        )
    
    @atomic
    def put(self, request, rule_id):
        rule = self.get_employer_bonus_rules(self.user, rule_id=rule_id)
        self.update_bonus_rule(self.user, rule, self.data)
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: 'Referral bonus rule updated'
            }
        )
    
    def delete(self, request, rule_id):
        rule = self.get_employer_bonus_rules(self.user, rule_id=rule_id)
        rule.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        rule.delete()
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: 'Referral bonus rule deleted'
            }
        )
    
    @staticmethod
    def get_employer_bonus_rules(user, rule_id=None, employer_id=None, is_use_permissions=True):
        filter = Q()
        if rule_id:
            filter &= Q(id=rule_id)
        elif employer_id:
            filter &= Q(employer_id=employer_id)
            
        rules = EmployerReferralBonusRule.objects\
            .select_related('bonus_currency')\
            .prefetch_related(
                'include_departments',
                'exclude_departments',
                'include_cities',
                'exclude_cities',
                'include_states',
                'exclude_states',
                'include_countries',
                'exclude_countries',
                'modifier'
            )\
            .filter(filter)
        
        if is_use_permissions:
            rules = EmployerReferralBonusRule.jv_filter_perm(user, rules)
        
        if rule_id:
            if not rules:
                raise EmployerReferralBonusRule.DoesNotExist
            return rules[0]
        
        return rules
    
    @staticmethod
    @atomic
    def update_bonus_rule(user, bonus_rule, data):
        data['bonus_currency_id'] = data['bonus_currency']['name']
        data['include_job_titles_regex'] = data['inclusion_criteria'].get('job_titles_regex')
        data['exclude_job_titles_regex'] = data['exclusion_criteria'].get('job_titles_regex')
        set_object_attributes(bonus_rule, data, {
            'order_idx': None,
            'include_job_titles_regex': None,
            'exclude_job_titles_regex': None,
            'base_bonus_amount': None,
            'bonus_currency_id': None,
            'days_after_hire_payout': None
        })
        
        permission_type = PermissionTypes.EDIT.value if bonus_rule.id else PermissionTypes.CREATE.value
        bonus_rule.jv_check_permission(permission_type, user)
        bonus_rule.save()
        
        # Clear existing criteria
        for field in [
            'include_departments', 'exclude_departments',
            'include_cities', 'exclude_cities',
            'include_states', 'exclude_states',
            'include_countries', 'exclude_countries'
        ]:
            bonus_rule_field = getattr(bonus_rule, field)
            bonus_rule_field.clear()
        
        for dataKey, prepend_text in (('inclusion_criteria', 'include_'), ('exclusion_criteria', 'exclude_')):
            for criteriaKey, criteriaVals in data[dataKey].items():
                if criteriaKey == 'job_titles_regex':
                    continue
                rule_key = f'{prepend_text}{criteriaKey}'
                bonus_rule_field = getattr(bonus_rule, rule_key)
                for val in criteriaVals:
                    bonus_rule_field.add(val['id'])
                    
        bonus_rule.modifier.all().delete()
        modifiers_to_save = []
        for modifier in data.get('modifiers'):
            modifiers_to_save.append(EmployerReferralBonusRuleModifier(
                referral_bonus_rule=bonus_rule,
                type=modifier['type'],
                amount=modifier['amount'],
                start_days_after_post=modifier['start_days_after_post']
            ))
        
        if modifiers_to_save:
            EmployerReferralBonusRuleModifier.objects.bulk_create(modifiers_to_save)
                    
                    
class EmployerBonusRuleOrderView(JobVyneAPIView):
    
    @atomic
    def put(self, request):
        rules = {
            r.id: r for r in
            EmployerBonusRuleView.get_employer_bonus_rules(self.user, employer_id=self.data['employer_id'])
        }
        rule_ids = self.data['rule_ids']
        if len(rules.values()) != len(rule_ids):
            return Response(
                'The length of the new rules order is not equal to the existing number of rules',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not rules:
            return Response(status=status.HTTP_200_OK)
        
        for order_idx, rule_id in enumerate(rule_ids):
            if not (rule := rules.get(rule_id)):
                return Response (
                    f'Rule with ID = {rule_id} does not exist for this employer'
                )
            
            if order_idx == 0:
                rule.jv_check_permission(PermissionTypes.EDIT.value, self.user)
            
            rule.order_idx = order_idx
            
        EmployerReferralBonusRule.objects.bulk_update(list(rules.values()), ['order_idx'])
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Referral bonus rules order updated'
        })


class EmployerAuthGroupView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    IGNORED_AUTH_GROUPS = [
        JobVyneUser.USER_TYPE_ADMIN, JobVyneUser.USER_TYPE_CANDIDATE,
        JobVyneUser.USER_TYPE_INFLUENCER  # TODO: Remove this one once influencer functionality is added
    ]
    
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
            auth_group_filter &= ~Q(user_type_bit__in=EmployerAuthGroupView.IGNORED_AUTH_GROUPS)
        return EmployerAuthGroup.objects.prefetch_related('permissions').filter(auth_group_filter)


class EmployerUserView(JobVyneAPIView):
    
    @atomic
    def post(self, request):
        user, is_new = UserView.get_or_create_user(self.user, self.data)
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
        users = UserView.get_user(self.user, user_filter=Q(id__in=self.data['user_ids']))
        batchCount = 0
        
        def get_unique_permission_key(p):
            return p.user_id, p.employer_id, p.permission_group_id
        
        while batchCount < len(users):
            user_employer_permissions_to_delete_filters = []
            user_employer_permissions_to_add = []
            user_employer_permissions_to_update = []
            for user in users[batchCount:batchCount + BATCH_UPDATE_SIZE]:
                set_object_attributes(user, self.data, {
                    'first_name': None,
                    'last_name': None
                })
                user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
                current_user_permissions = {
                    get_unique_permission_key(p): p for p in user.employer_permission_group.all()
                }
                
                if permission_group_ids := self.data.get('permission_group_ids'):
                    user_employer_permissions_to_delete_filters.append(
                        Q(user_id=user.id) & Q(employer_id=self.data['employer_id']))
                    for group_id in permission_group_ids:
                        user_employer_permissions_to_add.append(UserEmployerPermissionGroup(
                            user=user,
                            employer_id=self.data['employer_id'],
                            permission_group_id=group_id,
                            is_employer_approved=True
                        ))
                
                if add_permission_group_ids := self.data.get('add_permission_group_ids'):
                    for group_id in add_permission_group_ids:
                        permission_group = UserEmployerPermissionGroup(
                            user=user,
                            employer_id=self.data['employer_id'],
                            permission_group_id=group_id,
                            is_employer_approved=True
                        )
                        if existing_permission := current_user_permissions.get(
                                get_unique_permission_key(permission_group)):
                            existing_permission.is_employer_approved = True
                            user_employer_permissions_to_update.append(existing_permission)
                        else:
                            user_employer_permissions_to_add.append(permission_group)
                
                if remove_permission_group_ids := self.data.get('remove_permission_group_ids'):
                    for group_id in remove_permission_group_ids:
                        user_employer_permissions_to_delete_filters.append(
                            Q(user_id=user.id) & Q(permission_group_id=group_id))
            
            JobVyneUser.objects.bulk_update(users, ['first_name', 'last_name'])
            if user_employer_permissions_to_delete_filters:
                def reduceFilters(allFilters, filter):
                    allFilters |= filter
                    return allFilters
                
                delete_filter = reduce(reduceFilters, user_employer_permissions_to_delete_filters)
                UserEmployerPermissionGroup.objects.filter(delete_filter).delete()
            UserEmployerPermissionGroup.objects.bulk_create(user_employer_permissions_to_add)
            UserEmployerPermissionGroup.objects.bulk_update(user_employer_permissions_to_update,
                                                            ['is_employer_approved'])
            batchCount += BATCH_UPDATE_SIZE
        userCount = len(users)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'{userCount} {"user" if userCount == 1 else "users"} updated'
        })


class EmployerUserApproveView(JobVyneAPIView):
    
    @atomic
    def put(self, request):
        """Set unapproved permission groups to approved for selected users
        """
        users = UserView.get_user(self.user, user_filter=Q(id__in=self.data['user_ids']))
        groups_to_update = []
        for user in users:
            user.jv_check_permission(PermissionTypes.EDIT.value, self.user)
            for group in user.employer_permission_group.filter(is_employer_approved=False):
                group.is_employer_approved = True
                groups_to_update.append(group)
        
        UserEmployerPermissionGroup.objects.bulk_update(groups_to_update, ['is_employer_approved'])
        userCount = len(users)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: f'Permissions approved for {userCount} {"user" if userCount == 1 else "users"}'
        })


class EmployerUserActivateView(JobVyneAPIView):
    
    @atomic
    def put(self, request):
        is_deactivate = self.data['is_deactivate']
        users = UserView.get_user(self.user, user_filter=Q(id__in=self.data['user_ids']))
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
        employer_file = EmployerFile()
        file = self.files['file'][0] if self.files.get('file') else None
        self.update_employer_file(employer_file, self.data, self.user, file=file)
        return Response(status=status.HTTP_200_OK, data={
            'id': employer_file.id,
            SUCCESS_MESSAGE_KEY: f'Created a new file titled {employer_file.title}'
        })
    
    @atomic
    def put(self, request, file_id):
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


class EmployerJobLocationView(JobVyneAPIView):
    
    permission_classes = [IsAdminOrEmployerOrReadOnlyPermission]
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)

        job_filter = Q(employer_id=employer_id)
        jobs = EmployerJobView.get_employer_jobs(employer_job_filter=job_filter)
        cities, states, countries = {}, {}, {}
        for job in jobs:
            for location in job.locations.all():
                if location.city and not cities.get(location.city_id):
                    cities[location.city_id] = {'name': location.city.name, 'id': location.city.id}
                if location.state and not states.get(location.state_id):
                    states[location.state_id] = {'name': location.state.name, 'id': location.state.id}
                if location.country and not countries.get(location.country_id):
                    countries[location.country_id] = {'name': location.country.name, 'id': location.country.id}
        
        return Response(status=status.HTTP_200_OK, data={
            'cities': sorted(list(cities.values()), key=lambda x: x['name']),
            'states': sorted(list(states.values()), key=lambda x: x['name']),
            'countries': sorted(list(countries.values()), key=lambda x: x['name'])
        })
