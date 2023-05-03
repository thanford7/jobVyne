from jvapp.models.job_subscription import EmployerJobSubscription


def get_serialized_job_subscription(job_subscription: EmployerJobSubscription):
    return {
        'id': job_subscription.id,
        'employer_id': job_subscription.employer_id,
        'filters': {
            'job_title_regex': job_subscription.filter_job_title_regex,
            'exclude_job_title_regex': job_subscription.filter_exclude_job_title_regex,
            'cities': [{'name': c.name, 'id': c.id} for c in job_subscription.filter_city.all()],
            'states': [{'name': s.name, 'id': s.id} for s in job_subscription.filter_state.all()],
            'countries': [{'name': c.name, 'id': c.id} for c in job_subscription.filter_country.all()],
            'jobs': [{'title': j.job_title, 'id': j.id} for j in job_subscription.filter_job.all()],
            'employers': [{'name': e.employer_name, 'id': e.id} for e in job_subscription.filter_employer.all()],
            'remote_type_bit': job_subscription.filter_remote_type_bit
        }
    }
