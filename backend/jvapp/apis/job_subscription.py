from functools import reduce

from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.apis.geocoding import save_raw_location
from jvapp.apis.social import SocialLinkJobsView
from jvapp.models import JobVyneUser
from jvapp.models.employer import Employer
from jvapp.models.job_subscription import JobSubscription
from jvapp.models.abstract import PermissionTypes
from jvapp.serializers.job_subscription import get_serialized_job_subscription
from jvapp.serializers.location import get_serialized_location
from jvapp.utils.data import AttributeCfg, set_object_attributes


class JobSubscriptionView(JobVyneAPIView):
    
    def get(self, request):
        employer_id = self.query_params.get('employer_id')
        user_id = self.query_params.get('user_id')
        if not any((employer_id, user_id)):
            raise ValueError('An employer ID or user ID is required')
        
        if user_id:
            job_subscriptions = self.get_job_subscriptions(user_id=user_id)
        else:
            job_subscriptions = self.get_job_subscriptions(employer_id=employer_id)
        jobs_by_subscription = self.get_jobs_from_subscriptions(job_subscriptions)
        job_counts_by_subscription = [j.count() for j in jobs_by_subscription]
        serialized_subscriptions = [get_serialized_job_subscription(js) for js in job_subscriptions]
        for sub, job_count in zip(serialized_subscriptions, job_counts_by_subscription):
            sub['job_count'] = job_count
        
        return Response(status=status.HTTP_200_OK, data=serialized_subscriptions)
    
    def post(self, request):
        employer_id = self.data.get('employer_id')
        user_id = self.data.get('user_id')
        if not any((employer_id, user_id)):
            raise ValueError('An employer ID or user ID is required')
        
        job_subscription = JobSubscription(employer_id=employer_id, user_id=user_id)
        self.update_job_subscription(self.user, job_subscription, self.data)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully created job subscription'
        })
    
    def put(self, request, subscription_id=None):
        if not subscription_id:
            return get_error_response('A subscription ID is required')
        
        job_subscription = self.get_job_subscriptions(subscription_id=subscription_id)
        self.update_job_subscription(self.user, job_subscription, self.data)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully updated job subscription'
        })
    
    def delete(self, request, subscription_id=None):
        if not subscription_id:
            return get_error_response('A subscription ID is required')
        
        job_subscription = self.get_job_subscriptions(subscription_id=subscription_id)
        job_subscription.jv_check_permission(PermissionTypes.DELETE.value, self.user)
        job_subscription.delete()
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully deleted job subscription'
        })
    
    @staticmethod
    def get_job_subscriptions(subscription_id=None, employer_id=None, user_id=None):
        subscription_filter = Q()
        if subscription_id:
            subscription_filter &= Q(id=subscription_id)
        elif user_id:
            user = JobVyneUser.objects.get(id=user_id)
            # Get user's subscription and employee referral subscription
            subscription_filter &= (Q(user_id=user_id) | Q(employer_id=user.employer_id, is_single_employer=True))
        elif employer_id:
            subscription_filter &= Q(employer_id=employer_id)
        
        job_subscriptions = JobSubscription.objects \
            .prefetch_related(
                'filter_location',
                'filter_location__city',
                'filter_location__state',
                'filter_location__country',
                'filter_job',
                'filter_employer',
                'filter_job_titles'
            ) \
            .filter(subscription_filter)
        
        if subscription_id:
            if not job_subscriptions:
                raise JobSubscription.DoesNotExist
            return job_subscriptions[0]
        
        return job_subscriptions
    
    @staticmethod
    def update_job_subscription(user, job_subscription, data):
        # This requires an additional query so we can't execute it in the atomic block
        locations = []
        if raw_locations := data.get('locations'):
            for raw_location in raw_locations:
                locations.append(save_raw_location(raw_location, False))
        
        with atomic():
            set_object_attributes(job_subscription, data, {
                'title': None,
                'filter_remote_type_bit': AttributeCfg(form_name='remote_type_bit'),
                'filter_range_miles': AttributeCfg(form_name='range_miles')
            })
            
            permission_type = PermissionTypes.EDIT.value if job_subscription.id else PermissionTypes.CREATE.value
            job_subscription.jv_check_permission(permission_type, user)
            
            # Clear existing filters
            if job_subscription.id:
                if job_subscription.filter_location.all():
                    job_subscription.filter_location.clear()
                if job_subscription.filter_job.all():
                    job_subscription.filter_job.clear()
                if job_subscription.filter_employer.all():
                    job_subscription.filter_employer.clear()
            
            job_subscription.save()
            
            # Add new filters
            if job_title_ids := data.get('job_titles'):
                filter_job_titles = []
                filter_model = job_subscription.filter_job_titles.through
                for job_title_id in job_title_ids:
                    filter_job_titles.append(filter_model(
                        jobsubscription_id=job_subscription.id,
                        taxonomy_id=job_title_id
                    ))
                filter_model.objects.bulk_create(filter_job_titles)
            if locations:
                filter_locations = []
                filter_model = job_subscription.filter_location.through
                for location in locations:
                    filter_locations.append(filter_model(
                        jobsubscription_id=job_subscription.id,
                        location_id=location.id
                    ))
                filter_model.objects.bulk_create(filter_locations)
            if job_ids := data.get('jobs'):
                filter_jobs = []
                filter_model = job_subscription.filter_job.through
                for job_id in job_ids:
                    filter_jobs.append(filter_model(
                        jobsubscription_id=job_subscription.id,
                        employerjob_id=job_id
                    ))
                filter_model.objects.bulk_create(filter_jobs)
            if employer_ids := data.get('employers'):
                filter_employers = []
                filter_model = job_subscription.filter_employer.through
                for employer_id in employer_ids:
                    filter_employers.append(filter_model(
                        jobsubscription_id=job_subscription.id,
                        employer_id=employer_id
                    ))
                filter_model.objects.bulk_create(filter_employers)

    @staticmethod
    def get_jobs_from_subscriptions(job_subscriptions: iter):
        from jvapp.apis.employer import EmployerJobView  # Avoid circular import
        job_filters = [JobSubscriptionView.get_job_filter(js) for js in job_subscriptions]
        return [
            EmployerJobView.get_employer_jobs(employer_job_filter=jf)
            for jf in job_filters
        ]
    
    @staticmethod
    def get_combined_job_subscription_filter(job_subscriptions):
        if not job_subscriptions:
            return Q()
        job_filters = [JobSubscriptionView.get_job_filter(js) for js in job_subscriptions.all()]
        return reduce(lambda total, jf: total | jf, job_filters)
    
    @staticmethod
    def get_job_filter(job_subscription):
        job_filter = Q()
        if job_title_ids := [jt.id for jt in job_subscription.filter_job_titles.all()]:
            job_filter &= Q(taxonomy__taxonomy_id__in=job_title_ids)
        if job_ids := [j.id for j in job_subscription.filter_job.all()]:
            job_filter &= Q(id__in=job_ids)
        if employer_ids := [e.id for e in job_subscription.filter_employer.all()]:
            job_filter &= Q(employer_id__in=employer_ids)
    
        location_dicts = [get_serialized_location(l) for l in job_subscription.filter_location.all()]
        combined_location_filter = None
        if location_dicts:
            for location_dict in location_dicts:
                location_filter = SocialLinkJobsView.get_location_filter(
                    location_dict, job_subscription.filter_remote_type_bit or 0, job_subscription.filter_range_miles
                )
                if not combined_location_filter:
                    combined_location_filter = location_filter
                else:
                    combined_location_filter |= location_filter
        else:
            combined_location_filter = SocialLinkJobsView.get_location_filter(
                None, job_subscription.filter_remote_type_bit or 0, None
            )
        job_filter &= combined_location_filter
        return job_filter
    
    @staticmethod
    def get_or_create_employer_subscription(employer_id):
        """ Each employer has a unique job subscription that filters for all jobs
        connected to that employer
        """
        try:
            return JobSubscription.objects.get(employer_id=employer_id, is_single_employer=True)
        except JobSubscription.DoesNotExist:
            employer_subscription = JobSubscription(
                employer_id=employer_id,
                is_single_employer=True
            )
            employer_subscription.save()
            employer_subscription.filter_employer.add(employer_id)
            return employer_subscription
        
    @staticmethod
    def get_or_create_single_job_subscription(job_id):
        try:
            return JobSubscription.objects.get(job_id=job_id)
        except JobSubscription.DoesNotExist:
            job_subscription = JobSubscription(
                job_id=job_id
            )
            job_subscription.save()
            job_subscription.filter_job.add(job_id)
            return job_subscription
    
    @staticmethod
    def create_employer_subscription(employer_id):
        employer = Employer.objects.get(id=employer_id)
        employer_subscription = JobSubscription(
            employer_id=employer_id,
            is_single_employer=True,
            title=employer.employer_name
        )
        employer_subscription.save()
        employer_subscription.filter_employer.add(employer_id)
        return employer_subscription