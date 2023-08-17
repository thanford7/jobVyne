import json
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Count, F, Prefetch, Q, Sum, Value
from django.db.models.functions import Concat, TruncDate, TruncMonth, TruncWeek, TruncYear
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.employer import Employer, EmployerJob, Taxonomy
from jvapp.models.job_seeker import JobApplication
from jvapp.models.tracking import MessageThreadContext, PageView
from jvapp.models.user import JobVyneUser, UserApplicationReview
from jvapp.permissions.general import IsAdmin
from jvapp.serializers.location import get_serialized_location
from jvapp.serializers.tracking import get_serialized_message
from jvapp.utils.data import coerce_bool, coerce_int
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none


class BaseDataView(JobVyneAPIView):
    
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.start_dt = get_datetime_or_none(self.query_params.get('start_dt'))
        self.end_dt = get_datetime_or_none(self.query_params.get('end_dt'))
        self.timezone = self.end_dt.tzinfo if self.end_dt else timezone.utc
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
        self.page_count = coerce_int(self.query_params.get('page_count'), default=1)
        self.records_per_page = coerce_int(self.query_params.get('rows_per_page'), default=25)
        if not any([self.owner_id, self.employer_id]):
            raise ValueError('You must provide an owner ID, or employer ID')
    
    @staticmethod
    def get_link_data(social_link):
        if not social_link:
            return {}
        return {
            'link_id': social_link.id,
            'owner_id': social_link.owner_id,
            'owner_first_name': social_link.owner.first_name if social_link.owner else None,
            'owner_last_name': social_link.owner.last_name if social_link.owner else None,
            'link_name': social_link.name
        }


class ApplicationsView(BaseDataView):
    SORT_MAP = {
        'applicant': ('first_name',),
        'job_title': ('employer_job__job_title',),
        'email': ('email',),
        'created_dt': ('created_dt',),
        'source': ('social_link__owner__first_name', 'social_link__name'),
        'recommended': ('feedback_recommend_this_job',),
        'total_user_rating': ('total_user_rating',),
    }
    
    def get(self, request):
        if not self.user.is_admin:
            if self.employer_id and (self.user.employer_id or 0) != self.employer_id:
                return Response('You do not have access to this employer', status=status.HTTP_401_UNAUTHORIZED)
            if self.owner_id and self.user.id != self.owner_id:
                return Response('You do not have access to this user', status=status.HTTP_401_UNAUTHORIZED)
        is_exclude_job_board = self.query_params.get('is_exclude_job_board', False)
        applications = self.get_job_applications(
            self.user, start_date=self.start_dt, end_date=self.end_dt,
            employer_id=self.employer_id, owner_id=self.owner_id, is_ignore_permission=True,
            is_exclude_job_board=is_exclude_job_board
        )
        
        app_filter = Q()
        if self.filter_by:
            if employee_ids_filter := self.filter_by.get('employees'):
                app_filter &= Q(social_link__owner_id__in=employee_ids_filter)
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
            if source_filter := self.filter_by.get('sourceName'):
                app_filter &= (
                        Q(social_link__owner__first_name__iregex=f'^.*{source_filter}.*$') |
                        Q(social_link__owner__last_name__iregex=f'^.*{source_filter}.*$') |
                        Q(social_link__name__iregex=f'^.*{source_filter}.*$')
                )
            if locations_filter := self.filter_by.get('locations'):
                app_filter &= Q(employer_job__locations__in=locations_filter)
            if recommended_filter := self.filter_by.get('recommended'):
                rec_filter_q = Q(feedback_recommend_this_job__in=recommended_filter)
                if None in recommended_filter:
                    rec_filter_q |= Q(feedback_recommend_this_job__isnull=True)
                app_filter &= rec_filter_q
            if application_status_filter := self.filter_by.get('application_status'):
                app_filter &= Q(application_status=application_status_filter)
        
        applications = applications.filter(app_filter)
        
        if not self.is_raw_data:
            if 'owner_name' in self.group_by:
                self.group_by += ['owner_id', 'owner_first_name', 'owner_last_name']
            
            applications = applications \
                .annotate(date=TruncDate('created_dt', tzinfo=self.timezone)) \
                .annotate(week=TruncWeek('created_dt', tzinfo=self.timezone)) \
                .annotate(month=TruncMonth('created_dt', tzinfo=self.timezone)) \
                .annotate(year=TruncYear('created_dt', tzinfo=self.timezone)) \
                .annotate(platform_name=F('platform__name')) \
                .annotate(link_name=F('social_link__name')) \
                .annotate(owner_id=F('social_link__owner_id')) \
                .annotate(owner_first_name=F('social_link__owner__first_name')) \
                .annotate(owner_last_name=F('social_link__owner__last_name')) \
                .annotate(owner_name=Concat(
                    'social_link__owner__first_name', Value(' '), 'social_link__owner__last_name'
                )) \
                .annotate(applicant_name=Concat('first_name', Value(' '), 'last_name')) \
                .annotate(job_title=F('employer_job__job_title')) \
                .values(*self.group_by) \
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
        
        if not self.sort_order:
            sort_order = ('-created_dt',)
        else:
            sort_keys = self.SORT_MAP[self.sort_order]
            sort_order = []
            for key in sort_keys:
                sort_order.append(f'{"-" if self.is_sort_descending else ""}{key}')
                
        paged_applications = Paginator(applications.order_by(*sort_order), per_page=self.records_per_page)
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
        referrer = application.social_link.owner if application.social_link else application.referrer_user
        is_owner = referrer and (referrer.id == self.user.id)
        application_data = {
            'id': application.id,
            'job_title': application.employer_job.job_title,
            'email': application.email,
            'phone_number': application.phone_number,
            'linkedin_url': application.linkedin_url,
            'resume_url': application.resume.url if application.resume else None,
            'academic_transcript_url': application.academic_transcript.url if application.academic_transcript else None,
            'created_dt': get_datetime_format_or_none(application.created_dt),
            'locations': [get_serialized_location(l) for l in application.employer_job.locations.all()],
            'application_status': application.application_status
        }
        if is_employer or is_owner:
            application_data['first_name'] = application.first_name
            application_data['last_name'] = application.last_name
            application_data['feedback'] = {
                'feedback_know_applicant': application.feedback_know_applicant,
                'feedback_recommend_any_job': application.feedback_recommend_any_job,
                'feedback_recommend_this_job': application.feedback_recommend_this_job,
                'feedback_note': application.feedback_note
            }
        
        if is_employer:
            if referrer:
                application_data['referrer'] = {
                    'first_name': referrer.first_name,
                    'last_name': referrer.last_name,
                    'email': referrer.email
                }
            
            application_reviews = application.user_review.all()
            if personal_review := next((review for review in application_reviews if review.user_id == self.user.id), None):
                application_data['personal_rating'] = personal_review.rating
            application_data['ratings'] = sorted([
                {
                    'user_id': review.user_id,
                    'user_name': review.user.full_name,
                    'rating': review.rating
                } for review in application_reviews
            ], key=lambda x: x['rating'])
            
            application_data['message_threads'] = self.get_serialized_job_application_message_threads(application)
            
            application_data['notification_email_dt'] = get_datetime_format_or_none(application.notification_email_dt)
            application_data['notification_email_failure_dt'] = get_datetime_format_or_none(
                application.notification_email_failure_dt)
            application_data['notification_ats_dt'] = get_datetime_format_or_none(application.notification_ats_dt)
            application_data['notification_ats_failure_dt'] = get_datetime_format_or_none(
                application.notification_ats_failure_dt)
            application_data['notification_ats_failure_msg'] = application.notification_ats_failure_msg
        
        return {**application_data, **self.get_link_data(application.social_link)}
    
    @staticmethod
    def get_job_applications(
        user, start_date=None, end_date=None, employer_id=None, owner_id=None, is_exclude_job_board=False,
        is_ignore_permission=False
    ):
        app_filter = Q()
        if start_date:
            app_filter &= Q(created_dt__gte=start_date)
        if end_date:
            app_filter &= Q(created_dt__lte=end_date)
        if employer_id:
            app_filter &= Q(referrer_employer_id=employer_id)
        if owner_id:
            app_filter &= Q(referrer_user_id=owner_id)
        if is_exclude_job_board:
            app_filter &= Q(social_link__owner_id__isnull=False)
        
        # Include the message thread if this is the employer
        message_thread_prefetch = Prefetch(
            'message_thread_context',
            queryset=MessageThreadContext.objects
            .select_related('message_thread')
            .prefetch_related(
                'message_thread__message',
                'message_thread__message__recipient',
                'message_thread__message__attachment',
                'message_thread__message_groups'
            )
            .filter(
                message_thread__message_groups__employer_id__isnull=False,
                message_thread__message_groups__employer_id=employer_id,
                message_thread__message_groups__user_type_bits=JobVyneUser.USER_TYPE_EMPLOYER
            )
        )
        
        if user.is_employer:
            application_review_filter = Q(application__employer_job__employer_id=employer_id)
        else:
            application_review_filter = Q(application__referrer_user_id=user.id)
        application_review_prefetch = Prefetch(
            'user_review',
            queryset=UserApplicationReview.objects
            .select_related('application', 'application__employer_job', 'application__social_link', 'user')
            .filter(application_review_filter)
        )
        
        job_applications = JobApplication.objects \
            .select_related(
                'platform',
                'employer_job',
                'referrer_user',
                'referrer_employer',
                'social_link',
                'social_link__owner',
            ) \
            .prefetch_related(
                'employer_job__locations',
                'employer_job__locations__city',
                'employer_job__locations__state',
                'employer_job__locations__country',
                message_thread_prefetch,
                application_review_prefetch
            ) \
            .annotate(total_user_rating=Sum('user_review__rating')) \
            .filter(app_filter)
        
        if is_ignore_permission:
            return job_applications
        
        return JobApplication.jv_filter_perm(user, job_applications)
    
    @staticmethod
    def get_serialized_job_application_message_threads(job_application):
        message_thread_contexts = job_application.message_thread_context.all()
        message_threads = []
        for message_thread_context in message_thread_contexts:
            messages = []
            for message in message_thread_context.message_thread.message.all():
                messages.append(get_serialized_message(message))
            
            message_threads.append(messages)
        
        return message_threads


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
            link_data = tuple(pair for pair in self.get_link_data(view.social_link).items())
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
            view_filter &= (Q(social_link__employer_id=employer_id) | Q(employer_id=employer_id))
        if owner_id:
            view_filter &= (Q(social_link__owner_id=owner_id) | Q(page_owner_id=owner_id))
        views = PageView.objects \
            .select_related(
            'social_link',
            'social_link__owner'
        ) \
            .filter(view_filter)
        return PageView.jv_filter_perm(user, views)
    
    
class AdminDataProcessedJobsView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        job_filter = Q(close_date__isnull=True) | Q(close_date__gt=timezone.now().date())
        open_jobs = EmployerJob.objects.filter(job_filter)
        jobs_with_processed_description = open_jobs.filter(qualifications__isnull=False).count()
        jobs_with_profession = open_jobs.filter(taxonomy__taxonomy__tax_type=Taxonomy.TAX_TYPE_PROFESSION).count()
        employers = Employer.objects.filter(organization_type=Employer.ORG_TYPE_EMPLOYER)
        employers_with_description = employers.filter(description__isnull=False).count()
        
        return Response(status=status.HTTP_200_OK, data={
            'open_jobs_count': open_jobs.count(),
            'jobs_with_description_count': jobs_with_processed_description,
            'jobs_with_profession_count': jobs_with_profession,
            'employers_count': employers.count(),
            'employers_with_description_count': employers_with_description
        })
