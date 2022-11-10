import json
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Value
from django.db.models.functions import Concat, TruncDate, TruncMonth, TruncWeek, TruncYear
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import JobApplication, JobVyneUser, PageView
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none


class BaseDataView(JobVyneAPIView):
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.start_dt = get_datetime_or_none(self.query_params.get('start_dt'))
        self.end_dt = get_datetime_or_none(self.query_params.get('end_dt'))
        self.timezone = self.end_dt.tzinfo
        self.owner_id = self.query_params.get('owner_id')
        self.employer_id = self.query_params.get('employer_id')
        self.is_raw_data = self.query_params.get('is_raw_data')
        self.group_by = self.get_query_param_list('group_by', ['date'])
        self.filter_by = self.query_params.get('filter_by')
        if self.filter_by and isinstance(self.filter_by, str):
            self.filter_by = json.loads(self.filter_by)
        print(self.filter_by)
        self.page_count = self.query_params.get('page_count')
        self.q_filter = Q()
        if self.owner_id:
            owner_id = int(self.owner_id)
            self.q_filter &= Q(owner_id=owner_id)
        if self.employer_id:
            employer_id = int(self.employer_id)
            self.q_filter &= Q(employer_id=employer_id)
        if not any([self.owner_id, self.employer_id]):
            return Response('You must provide an owner ID, or employer ID', status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get_link_data(social_link):
        return {
            'link_id': social_link.id,
            'owner_id': social_link.owner_id,
            'owner_first_name': social_link.owner.first_name,
            'owner_last_name': social_link.owner.last_name,
            'platform_name': social_link.platform.name if social_link.platform else 'Unknown'
        }


class ApplicationsView(BaseDataView):
    
    def get(self, request):
        applications = self.get_job_applications(
            self.user, self.start_dt, self.end_dt,
            employer_id=self.employer_id, owner_id=self.owner_id
        )
        
        if not self.is_raw_data:
            if 'owner_name' in self.group_by:
                self.group_by += ['owner_id', 'owner_first_name', 'owner_last_name']
            
            appFilter = Q()
            if self.filter_by:
                if employee_ids := self.filter_by.get('employees'):
                    appFilter &= Q(social_link_filter__owner_id__in=employee_ids)
                if platforms := self.filter_by.get('platforms'):
                    appFilter &= Q(social_link_filter__platform__name__in=platforms)
                if job_title_search := self.filter_by.get('jobTitle'):
                    appFilter &= Q(employer_job__job_title__iregex=f'^.*{job_title_search}.*$')
            
            applications = applications\
                .filter(appFilter)\
                .annotate(date=TruncDate('created_dt', tzinfo=self.timezone))\
                .annotate(week=TruncWeek('created_dt', tzinfo=self.timezone))\
                .annotate(month=TruncMonth('created_dt', tzinfo=self.timezone))\
                .annotate(year=TruncYear('created_dt', tzinfo=self.timezone))\
                .annotate(platform_name=F('social_link_filter__platform__name')) \
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
        paged_applications = Paginator(applications, 25)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'total_page_count': paged_applications.num_pages,
                'total_application_count': paged_applications.count,
                'applications': [
                    self.serialize_application(app, is_employer)
                    for app in paged_applications.get_page(self.page_count)
                ]
            }
        )
    
    def serialize_application(self, application, is_employer):
        is_owner = application.social_link_filter.owner_id == self.user.id
        application_data = {
            'id': application.id,
            'job_title': application.employer_job.job_title,
            'apply_dt': get_datetime_format_or_none(application.created_dt),
        }
        if is_employer or is_owner:
            application_data['first_name'] = application.first_name
            application_data['last_name'] = application.last_name
        
        return {**application_data, **self.get_link_data(application.social_link_filter)}
    
    @staticmethod
    def get_job_applications(user, start_date, end_date, employer_id=None, owner_id=None):
        app_filter = Q(created_dt__lte=end_date) & Q(created_dt__gte=start_date)
        if employer_id:
            app_filter &= Q(social_link_filter__employer_id=employer_id)
        if owner_id:
            app_filter &= Q(social_link_filter__owner_id=owner_id)
        job_applications = JobApplication.objects \
            .select_related(
                'employer_job',
                'social_link_filter',
                'social_link_filter__owner',
                'social_link_filter__platform'
            ) \
            .filter(app_filter)
        
        return JobApplication.jv_filter_perm(user, job_applications)


class PageViewsView(BaseDataView):
    
    def get(self, request):
        
        # social_links = SocialLinkFilterView.get_link_filters(
        #     self.user, link_filter_filter=q_filter, start_dt=start_dt, end_dt=end_dt, is_use_permissions=False
        # )
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
                'social_link_filter__owner',
                'social_link_filter__platform'
            ). \
            filter(view_filter)
        return PageView.jv_filter_perm(user, views)
