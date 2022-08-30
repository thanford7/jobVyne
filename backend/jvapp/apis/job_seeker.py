from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.employer import EmployerBonusRuleView, EmployerJobView
from jvapp.apis.user import UserView
from jvapp.models import JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.job_seeker import JobApplication, JobApplicationTemplate
from jvapp.serializers.employer import get_serialized_employer_job
from jvapp.serializers.job_seeker import get_serialized_job_application
from jvapp.utils.data import AttributeCfg, set_object_attributes

__all__ = ('ApplicationView', 'ApplicationTemplateView')

APPLICATION_SAVE_CFG = {
    'first_name': None,
    'last_name': None,
    'email': None,
    'phone_number': None,
    'linkedin_url': None,
}


class ApplicationView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, application_id=None):
        if application_id:
            data = get_serialized_job_application(self.get_applications(application_id=application_id))
        elif user_id := self.query_params.get('user_id'):
            user = UserView.get_user(self.user, user_id=user_id)
            application_filter = Q(email=user.email)
            data = [
                get_serialized_job_application(ja)
                for ja in self.get_applications(application_filter=application_filter)
            ]
        elif employer_id := self.query_params.get('employer_id'):
            application_filter = Q(employer_job__employer_id=employer_id)
            data = [
                get_serialized_job_application(ja)
                for ja in self.get_applications(application_filter=application_filter)
            ]
        else:
            return Response('Unrecognized job application filter', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK, data=data)
    
    @atomic
    def post(self, request):
        email = self.data.get('email')
        job_id = self.data.get('job_id')
        if not all((email, job_id)):
            return Response('Email and job ID are required', status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has an account, but is not logged in
        if not self.user.is_authenticated:
            try:
                user = JobVyneUser.objects.get(email=email)
            except JobVyneUser.DoesNotExist:
                user = None
        else:
            user = self.user
        
        # Check if this person has already applied
        applications = self.get_applications(application_filter=Q(email=email, employer_job_id=job_id))
        if len(applications):
            return Response('You have already applied to this job', status=status.HTTP_400_BAD_REQUEST)
        
        # Save application to Django model
        application = JobApplication()
        resume = self.files['resume'][0] if self.files.get('resume') else None
        self.create_application(application, self.data, resume)
        
        if user:
            # Save or update application template to Django model
            application_template = ApplicationTemplateView.get_application_template(user.id) or JobApplicationTemplate()
            self.data['owner_id'] = user.id
            ApplicationTemplateView.create_or_update_application_template(
                application_template,
                self.data,
                resume,
                user
            )
            
            # Update user if they don't have the candidate bit set
            if not user.is_candidate:
                user.user_type_bits |= JobVyneUser.USER_TYPE_CANDIDATE
                user.save()
        
        # Push application to ATS integration
        
        # Refetch application to get related models
        application = self.get_applications(application_id=application.id)
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                SUCCESS_MESSAGE_KEY: f'Your application to {application.employer_job.employer.employer_name} for the {application.employer_job.job_title} position was submitted'
            }
        )
    
    @staticmethod
    @atomic
    def create_application(application, data, resume):
        cfg = {
            'employer_job_id': AttributeCfg(form_name='job_id'),
            'social_link_filter_id': AttributeCfg(form_name='filter_id'),
            **APPLICATION_SAVE_CFG
        }
        set_object_attributes(application, data, cfg)
        application.resume = resume or data.get('resume_url')
        
        ApplicationView.add_application_referral_bonus(application)
        application.save()
        
    @staticmethod
    def add_application_referral_bonus(application):
        job = EmployerJobView.get_employer_jobs(employer_job_id=application.employer_job_id)
        rules = EmployerBonusRuleView.get_employer_bonus_rules(None, employer_id=job.employer_id,
                                                               is_use_permissions=False)
        job = get_serialized_employer_job(job, rules=rules)
        application.referral_bonus = job['bonus']['amount'] or 0
        application.referral_bonus_currency_id = job['bonus']['currency']['name']
        application.referral_bonus_details = {
            'type': job['bonus']['type'],
            'bonus_rule': job['bonus_rule'],
            'job_bonus': {
                'amount': job['referral_bonus'],
                'currency': job['referral_bonus_currency']
            }
        }
    
    @staticmethod
    def get_applications(application_id=None, application_filter=None):
        if application_id:
            application_filter = Q(id=application_id)
        
        applications = JobApplication.objects \
            .select_related(
            'social_link_filter',
            'employer_job',
            'employer_job__employer'
        ) \
            .filter(application_filter)
        
        if application_id:
            if not applications:
                raise JobApplication.DoesNotExist
            return applications[0]
        
        return applications


class ApplicationTemplateView(JobVyneAPIView):
    
    def post(self, request):
        pass
    
    def put(self, request, application_template_id):
        pass
    
    @staticmethod
    @atomic
    def create_or_update_application_template(application_template, data, resume, user):
        cfg = {**APPLICATION_SAVE_CFG}
        if not application_template.id:
            cfg['owner_id'] = None
        
        set_object_attributes(application_template, data, cfg)
        if resume or (resume_url := data.get('resume_url')):
            application_template.resume = resume or resume_url
        permission_type = PermissionTypes.EDIT.value if application_template.id else PermissionTypes.CREATE.value
        application_template.jv_check_permission(permission_type, user)
        application_template.save()
        
    @staticmethod
    def get_application_template(owner_id):
        try:
            return JobApplicationTemplate.objects.get(owner_id=owner_id)
        except JobApplicationTemplate.DoesNotExist:
            return None
