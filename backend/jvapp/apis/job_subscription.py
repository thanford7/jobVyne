from functools import reduce

from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY, get_error_response
from jvapp.models.job_subscription import EmployerJobSubscription
from jvapp.models.abstract import PermissionTypes
from jvapp.serializers.employer import get_serialized_employer_job
from jvapp.serializers.job_subscription import get_serialized_job_subscription
from jvapp.utils.data import AttributeCfg, set_object_attributes


class EmployerJobSubscriptionView(JobVyneAPIView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return get_error_response('An employer ID is required')
        
        job_subscriptions = self.get_job_subscriptions(employer_id=employer_id)
        jobs_by_subscription = EmployerJobSubscriptionJobView.get_jobs_from_subscriptions(job_subscriptions, False)
        job_counts_by_subscription = [j.count() for j in jobs_by_subscription]
        serialized_subscriptions = [get_serialized_job_subscription(js) for js in job_subscriptions]
        for sub, job_count in zip(serialized_subscriptions, job_counts_by_subscription):
            sub['job_count'] = job_count
        
        return Response(status=status.HTTP_200_OK, data=serialized_subscriptions)
    
    def post(self, request):
        if not (employer_id := self.data.get('employer_id')):
            return get_error_response('An employer ID is required')
        
        job_subscription = EmployerJobSubscription(employer_id=employer_id)
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
    def get_job_subscriptions(subscription_id=None, employer_id=None):
        subscription_filter = Q()
        if subscription_id:
            subscription_filter &= Q(id=subscription_id)
        elif employer_id:
            subscription_filter &= Q(employer_id=employer_id)
        
        job_subscriptions = EmployerJobSubscription.objects \
            .prefetch_related(
            'filter_department',
            'filter_city',
            'filter_state',
            'filter_country',
            'filter_job',
            'filter_employer'
        ) \
            .filter(subscription_filter)
        
        if subscription_id:
            if not job_subscriptions:
                raise EmployerJobSubscription.DoesNotExist
            return job_subscriptions[0]
        
        return job_subscriptions
    
    @staticmethod
    @atomic
    def update_job_subscription(user, job_subscription, data):
        set_object_attributes(job_subscription, data, {
            'filter_remote_type_bit': AttributeCfg(form_name='remote_type_bit')
        })
        
        permission_type = PermissionTypes.EDIT.value if job_subscription.id else PermissionTypes.CREATE.value
        job_subscription.jv_check_permission(permission_type, user)
        
        # Clear existing filters
        if job_subscription.id:
            if job_subscription.filter_department.all():
                job_subscription.filter_department.clear()
            if job_subscription.filter_city.all():
                job_subscription.filter_city.clear()
            if job_subscription.filter_state.all():
                job_subscription.filter_state.clear()
            if job_subscription.filter_country.all():
                job_subscription.filter_country.clear()
            if job_subscription.filter_job.all():
                job_subscription.filter_job.clear()
            if job_subscription.filter_employer.all():
                job_subscription.filter_employer.clear()
        
        job_subscription.save()
        
        # Add new filters
        if department_ids := data.get('departments'):
            filter_departments = []
            filter_model = job_subscription.filter_department.through
            for department_id in department_ids:
                filter_departments.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    jobdepartment_id=department_id
                ))
            filter_model.objects.bulk_create(filter_departments)
        if city_ids := data.get('cities'):
            filter_cities = []
            filter_model = job_subscription.filter_city.through
            for city_id in city_ids:
                filter_cities.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    city_id=city_id
                ))
            filter_model.objects.bulk_create(filter_cities)
        if state_ids := data.get('states'):
            filter_states = []
            filter_model = job_subscription.filter_state.through
            for state_id in state_ids:
                filter_states.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    state_id=state_id
                ))
            filter_model.objects.bulk_create(filter_states)
        if country_ids := data.get('countries'):
            filter_countries = []
            filter_model = job_subscription.filter_country.through
            for country_id in country_ids:
                filter_countries.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    country_id=country_id
                ))
            filter_model.objects.bulk_create(filter_countries)
        if job_ids := data.get('jobs'):
            filter_jobs = []
            filter_model = job_subscription.filter_job.through
            for job_id in job_ids:
                filter_jobs.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    employerjob_id=job_id
                ))
            filter_model.objects.bulk_create(filter_jobs)
        if employer_ids := data.get('employers'):
            filter_employers = []
            filter_model = job_subscription.filter_employer.through
            for employer_id in employer_ids:
                filter_employers.append(filter_model(
                    employerjobsubscription_id=job_subscription.id,
                    employer_id=employer_id
                ))
            filter_model.objects.bulk_create(filter_employers)


class EmployerJobSubscriptionJobView(JobVyneAPIView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return get_error_response('An employer ID is required')
        
        job_subscriptions = EmployerJobSubscriptionView.get_job_subscriptions(employer_id=employer_id)
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_employer_job(j)
            for j in self.get_jobs_from_subscriptions(job_subscriptions, True)
        ])
    
    @staticmethod
    def get_jobs_from_subscriptions(job_subscriptions: iter, is_combined: bool):
        from jvapp.apis.employer import EmployerJobView  # Avoid circular import
        if is_combined:
            # Combine all filters into one
            job_filter = EmployerJobSubscriptionJobView.get_combined_job_subscription_filter(job_subscriptions)
            return EmployerJobView.get_employer_jobs(employer_job_filter=job_filter) if job_filter else []
        else:
            job_filters = [js.get_job_filter() for js in job_subscriptions]
            return [
                EmployerJobView.get_employer_jobs(employer_job_filter=jf)
                for jf in job_filters
            ]
    
    @staticmethod
    def get_combined_job_subscription_filter(job_subscriptions):
        if not job_subscriptions:
            return None
        job_filters = [js.get_job_filter() for js in job_subscriptions]
        return reduce(lambda total, jf: total | jf, job_filters)
