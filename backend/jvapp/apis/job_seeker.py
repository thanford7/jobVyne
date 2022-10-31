from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.ats import get_ats_api
from jvapp.apis.employer import EmployerBonusRuleView, EmployerJobView
from jvapp.apis.user import UserView
from jvapp.models import EmployerAts, JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.job_seeker import JobApplication, JobApplicationTemplate
from jvapp.models.user import UserEmployerCandidate
from jvapp.permissions.general import IsAuthenticatedOrPost
from jvapp.serializers.employer import get_serialized_employer_job
from jvapp.serializers.job_seeker import get_serialized_job_application
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.email import EMAIL_ADDRESS_SEND, get_attachment, get_encoded_file, send_email
from jvapp.utils.file import get_file_name, get_mime_from_in_memory_file

__all__ = ('ApplicationView', 'ApplicationTemplateView')

APPLICATION_SAVE_CFG = {
    'first_name': None,
    'last_name': None,
    'email': None,
    'phone_number': None,
    'linkedin_url': None,
}


class ApplicationView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrPost]
    
    def get(self, request, application_id=None):
        user_id = self.query_params.get('user_id')
        employer_id = self.query_params.get('employer_id')
        if application_id:
            data = get_serialized_job_application(self.get_applications(self.user, application_id=application_id))
        elif any([user_id, employer_id]):
            page_count = self.query_params.get('page_count')
            if user_id:
                user = UserView.get_user(self.user, user_id=user_id)
                application_filter = Q(user_id=user.id)
                if user.is_email_verified:
                    application_filter |= Q(email=user.email)
            else:
                application_filter = Q(employer_job__employer_id=employer_id)
            applications = self.get_applications(self.user, application_filter=application_filter)
            if page_count:
                paged_applications = Paginator(applications, per_page=25)
                data = {
                    'total_page_count': paged_applications.num_pages,
                    'applications': [get_serialized_job_application(ja) for ja in paged_applications.get_page(page_count)]
                }
            else:
                data = [
                    get_serialized_job_application(ja)
                    for ja in applications
                ]
        else:
            return Response('Unrecognized job application filter', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    def post(self, request):
        # Don't make this atomic in case the push to the ATS fails, we still want to capture the user's application
        email = self.data.get('email')
        job_id = self.data.get('job_id')
        if not all((email, job_id)):
            return Response('Email and job ID are required', status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has an account, but is not logged in
        # TODO: Consider always creating a user account if the applicant is new
        if not self.user.is_authenticated:
            try:
                user = JobVyneUser.objects.get(email=email)
            except JobVyneUser.DoesNotExist:
                user = None
        else:
            user = self.user
        
        # Check if this person has already applied
        applications = self.get_applications(
            self.user,
            application_filter=Q(email=email, employer_job_id=job_id),
            is_ignore_permissions=True
        )
        if len(applications):
            return Response('You have already applied to this job', status=status.HTTP_400_BAD_REQUEST)
        
        # Save application to Django model
        application = JobApplication()
        application_template = ApplicationTemplateView.get_application_template(user.id) if user else None
        if resume := self.files.get('resume'):
            resume = resume[0]
        elif application_template:
            resume = application_template.resume
        self.create_application(user, application, self.data, resume)
        send_email(
            'JobVyne | New application submission',
            to_emails=[email],
            from_email=EMAIL_ADDRESS_SEND,
            django_email_body_template='emails/application_submission_email.html',
            django_context={
                'application': application
            },
            attachments=[
                get_attachment(
                    get_file_name(application.resume.name),
                    get_encoded_file(application.resume.file.file),
                    get_mime_from_in_memory_file(application.resume.file.file),
                    get_file_name(application.resume.name)
                )
            ] if resume else None
        )
        
        if user:
            # Save or update application template to Django model
            application_template = application_template or JobApplicationTemplate()
            self.data['owner_id'] = user.id
            ApplicationTemplateView.create_or_update_application_template(
                application_template,
                self.data,
                application,
                user
            )
            
            # Update user if they don't have the candidate bit set
            if not user.is_candidate:
                user.user_type_bits |= JobVyneUser.USER_TYPE_CANDIDATE
                user.save()

        # Refetch application to get related models
        application = self.get_applications(
            self.user,
            application_id=application.id,
            is_ignore_permissions=True
        )
        
        # Push application to ATS integration
        if application.employer_job.ats_job_key:
            ats_cfg = EmployerAts.objects.get(employer_id=application.employer_job.employer_id)
            ats_api = get_ats_api(ats_cfg)
            ats_candidate_key, ats_application_key = ats_api.create_application(application)
            if user:
                try:
                    UserEmployerCandidate(
                        user=user,
                        employer=application.employer_job.employer,
                        ats_candidate_key=ats_candidate_key
                    ).save()
                except IntegrityError:
                    pass
                    
            application.ats_application_key = ats_application_key
            application.save()
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: f'Your application to {application.employer_job.employer.employer_name} for the {application.employer_job.job_title} position was submitted'
            }
        )
    
    @staticmethod
    @atomic
    def create_application(user, application, data, resume):
        application.user = user
        cfg = {
            'employer_job_id': AttributeCfg(form_name='job_id'),
            'social_link_filter_id': AttributeCfg(form_name='filter_id'),
            **APPLICATION_SAVE_CFG
        }
        set_object_attributes(application, data, cfg)
        application.resume = resume
        
        ApplicationView.add_application_referral_bonus(application)
        application.save()
        
    @staticmethod
    def add_application_referral_bonus(application):
        job = EmployerJobView.get_employer_jobs(employer_job_id=application.employer_job_id)
        rules = EmployerBonusRuleView.get_employer_bonus_rules(None, employer_id=job.employer_id,
                                                               is_use_permissions=False)
        job = get_serialized_employer_job(job, rules=rules, is_include_bonus=True)
        application.referral_bonus = job['bonus']['amount'] or 0
        application.referral_bonus_currency_id = job['bonus']['currency']['name']
        application.referral_bonus_details = {
            'type': job['bonus']['type'],
            'bonus_rule': job.get('bonus_rule', 'Default'),
            'job_bonus': {
                'amount': job['referral_bonus'],
                'currency': job['referral_bonus_currency']
            }
        }
    
    @staticmethod
    def get_applications(user, application_id=None, application_filter=None, is_ignore_permissions=False):
        if application_id:
            application_filter = Q(id=application_id)
        
        applications = JobApplication.objects \
            .prefetch_related(
                'employer_job__locations',
                'employer_job__locations__city',
                'employer_job__locations__state',
                'employer_job__locations__country',
            )\
            .select_related(
                'social_link_filter',
                'social_link_filter__owner',
                'employer_job',
                'employer_job__employer',
            ) \
            .filter(application_filter)
        
        if not is_ignore_permissions:
            applications = JobApplication.jv_filter_perm(user, applications)
        
        if application_id:
            if not applications:
                raise JobApplication.DoesNotExist
            return applications[0]
        
        return applications


class ApplicationTemplateView(JobVyneAPIView):
    
    @staticmethod
    @atomic
    def create_or_update_application_template(application_template, data, application, user):
        cfg = {**APPLICATION_SAVE_CFG}
        if not application_template.id:
            cfg['owner_id'] = None
        
        set_object_attributes(application_template, data, cfg)
        application_template.resume = application.resume
        permission_type = PermissionTypes.EDIT.value if application_template.id else PermissionTypes.CREATE.value
        application_template.jv_check_permission(permission_type, user)
        application_template.save()
        
    @staticmethod
    def get_application_template(owner_id):
        try:
            return JobApplicationTemplate.objects.get(owner_id=owner_id)
        except JobApplicationTemplate.DoesNotExist:
            return None
