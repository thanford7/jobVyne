from jvapp.models.job_subscription import JobSubscription
from jvapp.serializers.location import get_serialized_location


def get_serialized_job_subscription(job_subscription: JobSubscription):
    return {
        'id': job_subscription.id,
        'employer_id': job_subscription.employer_id,
        'is_single_employer': job_subscription.is_single_employer,
        'title': job_subscription.title,
        'filters': {
            'job_titles': [{'id': jt.id, 'name': jt.name} for jt in job_subscription.filter_job_titles.all()],
            'locations': [get_serialized_location(l) for l in job_subscription.filter_location.all()],
            'range_miles': job_subscription.filter_range_miles,
            'jobs': [{'title': j.job_title, 'id': j.id} for j in job_subscription.filter_job.all()],
            'employers': [{'name': e.employer_name, 'id': e.id} for e in job_subscription.filter_employer.all()],
            'remote_type_bit': job_subscription.filter_remote_type_bit
        }
    }
