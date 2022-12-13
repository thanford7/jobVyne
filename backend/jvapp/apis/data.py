import json
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Count, F, Prefetch, Q, Value
from django.db.models.functions import Concat, TruncDate, TruncMonth, TruncWeek, TruncYear
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import EmployerJob, JobApplication, JobVyneUser, MessageThreadContext, PageView
from jvapp.serializers.location import get_serialized_location
from jvapp.serializers.social import get_serialized_message_thread
from jvapp.utils.data import coerce_bool
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none


class BaseDataView(JobVyneAPIView):
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.start_dt = get_datetime_or_none(self.query_params.get('start_dt'))
        self.end_dt = get_datetime_or_none(self.query_params.get('end_dt'))
        self.timezone = self.end_dt.tzinfo
        self.owner_id = self.query_params.get('owner_id')
        if self.owner_id:
            self.owner_id = int(self.owner_id)
        self.employer_id = self.query_params.get('employer_id')
        if self.employer_id:
            self.employer_id = int(self.employer_id)
        self.is_raw_data = self.query_params.get('is_raw_data')
        self.group_by = self.get_query_param_list('group_by', ['date'])
        self.filter_by = self.query_params.get('filter_by')
        self.sort_order = self.query_params.get('sort_order')
        self.is_sort_descending = coerce_bool(self.query_params.get('is_descending'))
        if self.filter_by and isinstance(self.filter_by, str):
            self.filter_by = json.loads(self.filter_by)
        self.page_count = self.query_params.get('page_count')
        if not any([self.owner_id, self.employer_id]):
            raise ValueError('You must provide an owner ID, or employer ID')
    
    @staticmethod
    def get_link_data(social_link):
        return {
            'link_id': social_link.id,
            'owner_id': social_link.owner_id,
            'owner_first_name': social_link.owner.first_name,
            'owner_last_name': social_link.owner.last_name
        }


class ApplicationsView(BaseDataView):
    SORT_MAP = {
        'applicant': 'first_name',
        'job_title': 'employer_job__job_title',
        'email': 'email',
        'created_dt': 'created_dt',
        'referrer': 'social_link_filter__owner__first_name'
    }
    
    def get(self, request):
        if not self.user.is_admin:
            if self.employer_id and (self.user.employer_id or 0) != self.employer_id:
                return Response('You do not have access to this employer', status=status.HTTP_401_UNAUTHORIZED)
            if self.owner_id and self.user.id != self.owner_id:
                return Response('You do not have access to this user', status=status.HTTP_401_UNAUTHORIZED)
        applications = self.get_job_applications(
            self.user, self.start_dt, self.end_dt,
            employer_id=self.employer_id, owner_id=self.owner_id, is_ignore_permission=True
        )

        app_filter = Q()
        if self.filter_by:
            if employee_ids_filter := self.filter_by.get('employees'):
                app_filter &= Q(social_link_filter__owner_id__in=employee_ids_filter)
            if platforms_filter := self.filter_by.get('platforms'):
                app_filter &= Q(platform__name__in=platforms_filter)
            if job_title_search_filter := self.filter_by.get('jobTitle'):
                app_filter &= Q(employer_job__job_title__iregex=f'^.*{job_title_search_filter}.*$')
            if name_filter := self.filter_by.get('applicantName'):
                app_filter &= (
                    Q(first_name__iregex=f'^.*{name_filter}.*$') |
                    Q(last_name__iregex=f'^.*{name_filter}.*$')
                )
            if email_filter := self.filter_by.get('applicantEmail'):
                app_filter &= Q(email__iregex=f'^.*{email_filter}.*$')
            if referrer_filter := self.filter_by.get('referrerName'):
                app_filter &= (
                    Q(social_link_filter__owner__first_name__iregex=f'^.*{referrer_filter}.*$') |
                    Q(social_link_filter__owner__last_name__iregex=f'^.*{referrer_filter}.*$')
                )
            if locations_filter := self.filter_by.get('locations'):
                app_filter &= Q(employer_job__locations__in=locations_filter)
        
        applications = applications.filter(app_filter)
        
        if not self.is_raw_data:
            if 'owner_name' in self.group_by:
                self.group_by += ['owner_id', 'owner_first_name', 'owner_last_name']
            
            applications = applications\
                .annotate(date=TruncDate('created_dt', tzinfo=self.timezone))\
                .annotate(week=TruncWeek('created_dt', tzinfo=self.timezone))\
                .annotate(month=TruncMonth('created_dt', tzinfo=self.timezone))\
                .annotate(year=TruncYear('created_dt', tzinfo=self.timezone))\
                .annotate(platform_name=F('platform__name')) \
                .annotate(owner_id=F('social_link_filter__owner_id')) \
                .annotate(owner_first_name=F('social_link_filter__owner__first_name')) \
                .annotate(owner_last_name=F('social_link_filter__owner__last_name')) \
                .annotate(owner_name=Concat(
                    'social_link_filter__owner__first_name', Value(' '), 'social_link_filter__owner__last_name'
                ))\
                .annotate(applicant_name=Concat('first_name', Value(' '), 'last_name'))\
                .annotate(job_title=F('employer_job__job_title'))\
                .values(*self.group_by)\
                .annotate(count=Count('id'))
            
            if 'owner_name' in self.group_by:
                profile_pictures = {
                    u.id: u.profile_picture.url if u.profile_picture else None
                    for u in JobVyneUser.objects.filter(id__in=[a['owner_id'] for a in applications])
                }
                for app in applications:
                    app['owner_picture_url'] = profile_pictures.get(app['owner_id'])
            
            return Response(status=status.HTTP_200_OK, data=applications)
        
        is_employer = self.user.is_employer and self.employer_id and self.user.employer_id == self.employer_id
        sort_order = f'{"-" if self.is_sort_descending else ""}{self.SORT_MAP[self.sort_order]}' if self.sort_order else '-created_dt'
        paged_applications = Paginator(applications.order_by(sort_order), 25)
        locations = set()
        for app in applications:
            for location in app.employer_job.locations.all():
                locations.add(location)
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                'total_page_count': paged_applications.num_pages,
                'total_application_count': paged_applications.count,
                'applications': [
                    self.serialize_application(app, is_employer)
                    for app in paged_applications.get_page(self.page_count)
                ],
                'locations': [get_serialized_location(l) for l in locations]
            }
        )
    
    def serialize_application(self, application, is_employer):
        is_owner = application.social_link_filter.owner_id == self.user.id
        application_data = {
            'id': application.id,
            'job_title': application.employer_job.job_title,
            'email': application.email,
            'phone_number': application.phone_number,
            'linkedin_url': application.linkedin_url,
            'resume_url': application.resume.url if application.resume else None,
            'created_dt': get_datetime_format_or_none(application.created_dt),
            'locations': [get_serialized_location(l) for l in application.employer_job.locations.all()]
        }
        if is_employer or is_owner:
            application_data['first_name'] = application.first_name
            application_data['last_name'] = application.last_name
            
        if is_employer:
            application_data['notification_email_dt'] = get_datetime_format_or_none(application.notification_email_dt)
            application_data['notification_email_failure_dt'] = get_datetime_format_or_none(application.notification_email_failure_dt)
            application_data['notification_ats_dt'] = get_datetime_format_or_none(application.notification_ats_dt)
            application_data['notification_ats_failure_dt'] = get_datetime_format_or_none(application.notification_ats_failure_dt)
            application_data['notification_ats_failure_msg'] = get_datetime_format_or_none(application.notification_ats_failure_msg)
        
        return {**application_data, **self.get_link_data(application.social_link_filter)}
    
    @staticmethod
    def get_job_applications(user, start_date, end_date, employer_id=None, owner_id=None, is_ignore_permission=False):
        app_filter = Q(created_dt__lte=end_date) & Q(created_dt__gte=start_date)
        if employer_id:
            app_filter &= Q(social_link_filter__employer_id=employer_id)
        if owner_id:
            app_filter &= Q(social_link_filter__owner_id=owner_id)
        
        # Include the message thread if this is the employer
        message_thread_prefetch = Prefetch(
            'message_thread_context',
            queryset=MessageThreadContext.objects
                .select_related('message_thread')
                .prefetch_related('message_thread__message', 'message_thread__message__recipient')
                .filter(message_thread__employer_id__isnull=False, message_thread__employer_id=employer_id)
        )
        
        job_applications = JobApplication.objects \
            .select_related(
                'platform',
                'employer_job',
                'social_link_filter',
                'social_link_filter__owner',
            ) \
            .prefetch_related(
                'employer_job__locations',
                'employer_job__locations__city',
                'employer_job__locations__state',
                'employer_job__locations__country',
                message_thread_prefetch
            ) \
            .filter(app_filter)
        
        if is_ignore_permission:
            return job_applications
        
        return JobApplication.jv_filter_perm(user, job_applications)


class PageViewsView(BaseDataView):
    
    def get(self, request):
        link_views = self.get_link_views(
            self.user, self.start_dt, self.end_dt,
            employer_id=self.employer_id, owner_id=self.owner_id
        )

        if not self.is_raw_data:
            link_views = link_views \
                .annotate(date=TruncDate('access_dt', tzinfo=self.timezone)) \
                .annotate(week=TruncWeek('access_dt', tzinfo=self.timezone)) \
                .annotate(month=TruncMonth('access_dt', tzinfo=self.timezone)) \
                .annotate(year=TruncYear('access_dt', tzinfo=self.timezone)) \
                .values(*self.group_by) \
                .annotate(count=Count('id'))
    
            return Response(status=status.HTTP_200_OK, data=link_views)
        
        # TODO: Apply group by and then use paginator to return data
        views = defaultdict(int)
        for view in link_views:
            link_data = tuple(pair for pair in self.get_link_data(view.social_link_filter).items())
            views[(
                get_datetime_format_or_none(view.access_dt),
                bool(view.is_mobile or view.is_tablet),
                link_data
            )] += 1
        
        serialized_views = []
        for view_key, view_count in views.items():
            link_data = {key: val for key, val in view_key[2]}
            serialized_views.append({
                'access_dt': view_key[0],
                'is_mobile': view_key[1],
                **link_data,
                'view_count': view_count,
            })
        
        return Response(status=status.HTTP_200_OK, data=serialized_views)
    
    @staticmethod
    def get_link_views(user, start_date, end_date, employer_id=None, owner_id=None):
        view_filter = Q(access_dt__lte=end_date) & Q(access_dt__gte=start_date)
        if employer_id:
            view_filter &= Q(social_link_filter__employer_id=employer_id)
        if owner_id:
            view_filter &= Q(social_link_filter__owner_id=owner_id)
        views = PageView.objects \
            .select_related(
                'social_link_filter',
                'social_link_filter__owner'
            )\
            .filter(view_filter)
        return PageView.jv_filter_perm(user, views)
