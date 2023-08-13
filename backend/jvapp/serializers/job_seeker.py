from django.utils import timezone

from jvapp.models.job_seeker import *
from jvapp.serializers.location import get_serialized_location
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
        'resume_url': app.resume.url if app.resume else None,
        'academic_transcript_url': app.academic_transcript.url if app.academic_transcript else None
    }


def get_serialized_job_application(job_application: JobApplication):
    from jvapp.apis.social import SocialLinkView
    # TODO: Not performant
    job_link = SocialLinkView.get_or_create_single_job_link(job_application.employer_job)
    data = {
        **base_application_serializer(job_application),
        'social_link_id': job_application.social_link_id,
        # If application is external, the applicant can edit the application status manually
        # since we can't update it from the ATS or JobVyne job tracking
        'is_external_application': job_application.is_external_application,
        'application_status': job_application.application_status,
        'employer_job': {
            'id': job_application.employer_job_id,
            'url': job_link.get_link_url(),
            'employer_name': job_application.employer_job.employer.employer_name,
            'employer_id': job_application.employer_job.employer_id,
            'employer_key': job_application.employer_job.employer.employer_key,
            'title': job_application.employer_job.job_title,
            'locations': [get_serialized_location(l) for l in job_application.employer_job.locations.all()],
            'is_open': (not job_application.employer_job.close_date) or (job_application.employer_job.close_date < timezone.now().date())
        }
    }
    return data
