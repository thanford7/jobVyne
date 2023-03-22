from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, WARNING_MESSAGES_KEY, get_error_response
from jvapp.apis.job_subscription import EmployerJobSubscriptionJobView, EmployerJobSubscriptionView
from jvapp.models import JobApplication, Message, PageView, REMOTE_TYPES
from jvapp.models.abstract import PermissionTypes
from jvapp.models.social import *
from jvapp.serializers.employer import get_serialized_employer, get_serialized_employer_job
from jvapp.serializers.social import *
from jvapp.serializers.social import get_serialized_link_tag
from jvapp.utils.data import AttributeCfg, coerce_int, set_object_attributes

__all__ = ('SocialPlatformView', 'SocialLinkFilterView', 'SocialLinkJobsView', 'ShareSocialLinkView')

from jvapp.utils.email import send_django_email
from jvapp.utils.message import send_sms_message
from jvapp.utils.sanitize import sanitize_html


class SocialPlatformView(JobVyneAPIView):
    
    def get(self, request):
        data = [get_serialized_social_platform(sp) for sp in SocialPlatform.objects.all()]
        return Response(status=status.HTTP_200_OK, data=data)


class SocialLinkFilterView(JobVyneAPIView):
    
    def get(self, request, link_filter_id=None):
        if link_filter_id:
            data = get_serialized_social_link_filter(self.get_link_filters(self.user, link_filter_id=link_filter_id))
        else:
            if owner_id := self.query_params.get('owner_id'):
                q_filter = Q(owner_id=owner_id)
            elif employer_id := self.query_params.get('employer_id'):
                q_filter = Q(employer_id=employer_id, owner_id__isnull=True)
            else:
                return Response('You must provide an ID, owner ID, or employer ID', status=status.HTTP_400_BAD_REQUEST)
            
            data = []
            for link_filter in self.get_link_filters(self.user, link_filter_filter=q_filter):
                serialized_link_filter = get_serialized_social_link_filter(link_filter, is_include_performance=True)
                # Only fetch job count for specific user because a database call
                # is required per link_filter and is not performant
                if owner_id:
                    serialized_link_filter['jobs_count'] = len(
                        SocialLinkJobsView.get_jobs_from_filter(link_filter=link_filter))
                data.append(serialized_link_filter)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        new_link = SocialLinkFilter()
        new_link, is_duplicate = self.create_or_update_link_filter(new_link, self.data, self.user)
        is_get_or_create = self.data.get('is_get_or_create')
        data = {}
        # Sometimes we want to silently get or create a link (e.g. when a user is sharing an individual job)
        if not is_get_or_create:
            if is_duplicate and not self.data.get('is_default'):
                data = {
                    WARNING_MESSAGES_KEY: ['A referral link with these filters already exists']
                }
            elif is_duplicate:
                data = {
                    SUCCESS_MESSAGE_KEY: 'A referral link with these filters already exists. The default property was updated'
                }
            else:
                data = {
                    SUCCESS_MESSAGE_KEY: 'Created a new job link'
                }
        if is_get_or_create:
            data['link_filter'] = get_serialized_social_link_filter(new_link)
        else:
            data['id'] = new_link.id
        return Response(status=status.HTTP_200_OK, data=data)
    
    def put(self, request):
        if not (link_filter_id := self.data.get('link_filter_id')):
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        link = self.get_link_filters(self.user, link_filter_id=link_filter_id)
        self.create_or_update_link_filter(link, self.data, self.user)
        
        # Need to refetch to get associated objects
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'The job link was successfully updated'
        })
    
    @atomic
    def delete(self, request):
        link_filter_id = self.data.get('link_filter_id')
        link_filter_ids = [link_filter_id] if link_filter_id else self.data.get('link_filter_ids')
        if not link_filter_ids:
            return Response('A link filter ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        links = self.get_link_filters(self.user, link_filter_filter=Q(id__in=link_filter_ids))
        for link in links:
            link.jv_check_permission(PermissionTypes.DELETE.value, self.user)
            link.is_archived = True
        SocialLinkFilter.objects.bulk_update(links, ['is_archived'])
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully archived job link'
        })
    
    @staticmethod
    @atomic
    def create_or_update_link_filter(link_filter, data, user=None):
        """ Create or update a link filter.
        :return {bool}: If True, the link filter is a duplicate
        """
        cfg = {
            'is_default': AttributeCfg(is_ignore_excluded=True),
            'name': AttributeCfg(form_name='link_name', is_ignore_excluded=True)
        }
        is_new = not link_filter.created_dt
        is_duplicate = False

        # Add owner and employer for new link
        if is_new:
            cfg = {
                'owner_id': None,
                'employer_id': None,
                **cfg
            }
        
        set_object_attributes(link_filter, data, cfg)
        
        if user:
            permission_type = PermissionTypes.EDIT.value if link_filter.id else PermissionTypes.CREATE.value
            link_filter.jv_check_permission(permission_type, user)
        link_filter.save()
        
        if department_ids := data.get('department_ids'):
            link_filter.departments.set(department_ids)
        
        if city_ids := data.get('city_ids'):
            link_filter.cities.set(city_ids)
        
        if state_ids := data.get('state_ids'):
            link_filter.states.set(state_ids)
        
        if country_ids := data.get('country_ids'):
            link_filter.countries.set(country_ids)
        
        if job_ids := data.get('job_ids'):
            link_filter.jobs.set(job_ids)
            
        if link_tags := data.get('link_tags'):
            normalized_link_tags = []
            for link_tag in link_tags:
                normalized_link_tags.append(
                    SocialLinkTagView.get_or_create_link_tag(user, link_tag, link_filter.employer_id, link_filter.owner_id)
                )
            link_filter.tags.set(normalized_link_tags)
        
        existing_filters = SocialLinkFilterView.get_user_existing_filters(
            user, link_filter.owner_id, current_link_filter_id=link_filter.id
        )
        
        # Remove default flag from previous filters
        if link_filter.is_default:
            for filter in existing_filters.values():
                if filter.is_default:
                    filter.is_default = False
                    filter.save()
        
        # Make sure this isn't a duplicate filter
        existing_filter = existing_filters.get(link_filter.get_unique_key())
        if existing_filter:
            # If this is a new filter, we don't have to worry about FK associations (e.g. job applications) and
            # can just delete the new filter to prevent a duplicate
            if is_new:
                existing_filter.is_default = link_filter.is_default
                existing_filter.is_primary = link_filter.is_primary
                existing_filter.save()
                link_filter.delete()
            else:
                raise ValueError('A referral link with these filters already exists')
            is_duplicate = True
        
        return (existing_filter or link_filter), is_duplicate
    
    @staticmethod
    def get_user_existing_filters(user, owner_id, current_link_filter_id=None):
        return {
            f.get_unique_key(): f for f in
            SocialLinkFilterView.get_link_filters(
                user, link_filter_filter=Q(owner_id=owner_id), is_use_permissions=False
            ) if (f.id != current_link_filter_id or not current_link_filter_id)
        }
    
    @staticmethod
    def get_link_filters(
            user, link_filter_id=None, link_filter_filter=None, start_dt=None, end_dt=None, is_use_permissions=True
    ):
        if link_filter_id:
            link_filter_filter = Q(id=link_filter_id)
        elif (not link_filter_id) and link_filter_filter:
            link_filter_filter &= Q(is_archived=False)
        
        app_filter = Q()
        view_filter = Q()
        if start_dt:
            app_filter &= Q(created_dt__gte=start_dt)
            view_filter &= Q(access_dt__gte=start_dt)
        if end_dt:
            app_filter &= Q(created_dt__lte=end_dt)
            view_filter &= Q(access_dt__lte=end_dt)
        
        app_prefetch = Prefetch(
            'job_application',
            queryset=JobApplication.objects.select_related('employer_job').filter(app_filter)
        )
        
        page_view_prefetch = Prefetch(
            'page_view',
            queryset=PageView.objects.filter(view_filter)
        )
        
        links = SocialLinkFilter.objects \
            .select_related('employer', 'owner') \
            .prefetch_related(
                'departments', 'cities', 'states', 'countries', 'jobs', 'tags',
                app_prefetch, page_view_prefetch
            ) \
            .filter(link_filter_filter)
        
        if is_use_permissions:
            links = SocialLinkFilter.jv_filter_perm(user, links)
        
        if link_filter_id:
            if not links:
                raise SocialLinkFilter.DoesNotExist
            return links[0]
        
        return links


class SocialLinkJobsView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, link_filter_id=None):
        from jvapp.apis.employer import EmployerView  # Avoid circular import
        page_count = self.query_params.get('page_count', 1)
        employer_id = self.query_params.get('employer_id')
        if not any([link_filter_id, employer_id]):
            raise ValueError('A link filter ID or employer ID is required')
        
        link_filter = SocialLinkFilterView.get_link_filters(
            self.user,
            link_filter_id=link_filter_id,
            is_use_permissions=False  # This is a public page
        ) if link_filter_id else None
        
        employer_id = link_filter.employer_id if link_filter else employer_id
        
        jobs = self.get_jobs_from_filter(
            link_filter=link_filter,
            employer_id=employer_id,
            filter_values=self.get_filter_values_from_query_params()
        )
        total_jobs = self.get_jobs_from_filter(employer_id=employer_id, filter_values={}).count()
        paged_jobs = Paginator(jobs, per_page=5)
        employer = EmployerView.get_employers(employer_id=employer_id)
        has_job_subscription = bool(EmployerJobSubscriptionView.get_job_subscriptions(employer_id=employer_id).count())
        return Response(status=status.HTTP_200_OK, data={
            'total_page_count': paged_jobs.num_pages,
            'total_employer_job_count': total_jobs,
            'has_job_subscription': has_job_subscription,
            'jobs': [get_serialized_employer_job(j) for j in paged_jobs.get_page(page_count)],
            'employer': get_serialized_employer(employer),
            'owner_id': link_filter.owner_id if link_filter else None,
            'is_active_employee': link_filter.owner.is_active_employee if (link_filter and link_filter.owner) else True,
            'filter_values': link_filter.get_filter_values() if link_filter else self.get_filter_values_from_query_params()
        })
    
    def get_filter_values_from_query_params(self):
        filter_values = {}
        if job_title := self.query_params.get('job_title'):
            filter_values['job_title'] = job_title
        if city_ids := self.query_params.getlist('city_ids[]'):
            filter_values['city_ids'] = [int(city_id) for city_id in city_ids]
        if state_ids := self.query_params.getlist('state_ids[]'):
            filter_values['state_ids'] = [int(state_id) for state_id in state_ids]
        if country_ids := self.query_params.getlist('country_ids[]'):
            filter_values['country_ids'] = [int(country_id) for country_id in country_ids]
        if department_ids := self.query_params.getlist('department_ids[]'):
            filter_values['department_ids'] = [int(department_id) for department_id in department_ids]
        if job_ids := self.query_params.getlist('job_ids[]'):
            filter_values['job_ids'] = [int(job_id) for job_id in job_ids]
        if remote_type_bit := self.query_params.get('remote_type_bit'):
            filter_values['remote_type_bit'] = coerce_int(remote_type_bit)
        if minimum_salary := self.query_params.get('minimum_salary'):
            filter_values['minimum_salary'] = coerce_int(minimum_salary)
        
        return filter_values
    
    @staticmethod
    def get_jobs_from_filter(link_filter=None, employer_id=None, filter_values=None):
        if not any([link_filter, employer_id]):
            raise ValueError('A link filter or employer ID is required')
        if filter_values is None and link_filter:
            filter_values = link_filter.get_filter_values()
        employer_id = employer_id or link_filter.employer_id
        return SocialLinkJobsView.get_filtered_jobs(employer_id, **filter_values)
    
    @staticmethod
    def get_filtered_jobs(
        employer_id, department_ids=None, city_ids=None, state_ids=None, country_ids=None,
        job_ids=None, job_title=None, remote_type_bit=None, minimum_salary=None
    ):
        from jvapp.apis.employer import EmployerJobView  # Avoid circular import
        
        job_subscriptions = EmployerJobSubscriptionView.get_job_subscriptions(employer_id=employer_id)
        if job_subscriptions:
            subscription_filters = EmployerJobSubscriptionJobView.get_combined_job_subscription_filter(
                job_subscriptions
            )
            jobs_filter = (Q(employer_id=employer_id) | subscription_filters)
        else:
            jobs_filter = Q(employer_id=employer_id)
        
        if department_ids:
            jobs_filter &= Q(job_department_id__in=department_ids)
        if city_ids:
            jobs_filter &= Q(locations__city_id__in=city_ids)
        if state_ids:
            jobs_filter &= Q(locations__state_id__in=state_ids)
        if country_ids:
            jobs_filter &= Q(locations__country_id__in=country_ids)
        if job_ids:
            jobs_filter &= Q(id__in=job_ids)
        if job_title:
            jobs_filter &= Q(job_title__iregex=f'^.*{job_title}.*$')
        if remote_type_bit:
            if remote_type_bit == REMOTE_TYPES.YES:
                jobs_filter &= Q(locations__is_remote=True)
            elif remote_type_bit == REMOTE_TYPES.NO:
                jobs_filter &= Q(locations__is_remote=False)
        if minimum_salary:
            # Some jobs have a salary floor but no ceiling so we check for both
            jobs_filter &= (Q(salary_ceiling__gte=minimum_salary) | Q(salary_floor__gte=minimum_salary))
        
        return EmployerJobView.get_employer_jobs(employer_job_filter=jobs_filter)


class ShareSocialLinkView(JobVyneAPIView):
    
    def post(self, request):
        job_link = SocialLinkFilterView.get_link_filters(self.user, link_filter_id=self.data['socialLinkId'])
        if self.user.id != job_link.owner_id:
            return get_error_response('You do not have access to this job link')
        share_type = self.data['shareType']
        if share_type == Message.MessageType.EMAIL.value:
            send_django_email(
                self.data['emailSubject'], 'emails/base_general_email.html',
                to_email=self.data['toEmail'], from_email=self.data['fromEmail'],
                html_body_content=sanitize_html(f'<p>{self.data["emailBody"]}</p>', is_email=True),
                django_context={
                    'is_exclude_final_message': True
                }
            )
            
            return Response(status=status.HTTP_200_OK, data={
                SUCCESS_MESSAGE_KEY: f'Message sent to {self.data["toEmail"]}'
            })
        elif share_type == Message.MessageType.SMS.value:
            send_sms_message(self.data['textBody'], self.data['phoneNumber'])
            return Response(status=status.HTTP_200_OK, data={
                SUCCESS_MESSAGE_KEY: f'Message sent to {self.data["phoneNumber"]}'
            })
        

class SocialLinkTagView(JobVyneAPIView):
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        owner_id = self.query_params.get('owner_id')
        if not any([employer_id, owner_id]):
            return get_error_response('An employer ID or owner ID is required')
        
        link_tags = self.get_link_tags(self.user, employer_id=employer_id, owner_id=owner_id)
        return Response(status=status.HTTP_200_OK, data=[get_serialized_link_tag(lt) for lt in link_tags])
    
    @staticmethod
    def get_link_tags(user, employer_id=None, owner_id=None):
        assert any([employer_id, owner_id])
        link_tag_filter = Q()
        if employer_id:
            link_tag_filter = Q(employer_id=employer_id)
        if owner_id:
            link_tag_filter = Q(owner_id=owner_id)
        link_tag_filters = SocialLinkTag.objects.filter(link_tag_filter)
        return SocialLinkTag.jv_filter_perm(user, link_tag_filters)
    
    @staticmethod
    def get_or_create_link_tag(user, tag_name, employer_id, owner_id):
        link_tag = SocialLinkTag.objects.filter(tag_name=tag_name, employer_id=employer_id, owner_id=owner_id)
        if link_tag:
            link_tag = SocialLinkTag.jv_filter_perm(user, link_tag)
            return link_tag[0]
        
        link_tag = SocialLinkTag(tag_name=tag_name, employer_id=employer_id, owner_id=owner_id)
        link_tag.jv_check_permission(PermissionTypes.CREATE.value, user)
        link_tag.save()
        return link_tag
        
        