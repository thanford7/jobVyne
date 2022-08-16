from jvapp.models.job_seeker import *
from jvapp.utils.datetime import get_datetime_format_or_none


def base_application_serializer(app: JobApplication or JobApplicationTemplate):
    return {
        'id': app.id,
        'created_dt': get_datetime_format_or_none(app.created_dt),
        'first_name': app.first_name,
        'last_name': app.last_name,
        'email': app.email,
        'phone_number': app.phone_number,
        'linkedin_url': app.linkedin_url,
        'resume_url': app.resume.url if app.resume else None
    }


def get_serialized_job_application(job_application: JobApplication):
    return {
        **base_application_serializer(job_application),
        'social_link_filter_id': job_application.social_link_filter_id,
        'employer_job': {
            'id': job_application.employer_job_id,
            'employer_name': job_application.employer_job.employer.employer_name,
            'employer_id': job_application.employer_job.employer_id,
            'title': job_application.employer_job.job_title
        }
    }
