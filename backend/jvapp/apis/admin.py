from django.db.models import Count, Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.user import UserView
from jvapp.models import Employer, EmployerAuthGroup, JobVyneUser, UserEmployerPermissionGroup
from jvapp.permissions.general import IsAdmin
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.datetime import get_datetime_format_or_none
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT


class EmployerView(JobVyneAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request, employer_id=None):
        employer_id = employer_id or self.data.get('employer_id')
        if employer_id:
            employer = self.get_employers(employer_id=employer_id)
            return Response(status=status.HTTP_200_OK, data=self.get_serialized_employer(employer))
        employers = self.get_employers(employer_filter=Q())
        return Response(status=status.HTTP_200_OK, data=[
            self.get_serialized_employer(employer) for employer in employers
        ])
    
    @atomic
    def post(self, request):
        # Create employer
        employer = Employer()
        set_object_attributes(employer, self.data, {
            'employer_name': AttributeCfg(form_name='name'),
            'email_domains': None
        })
        employer.logo = self.files.get('logo')[0] if self.files.get('logo') else None
        employer.save()
        
        # Create account owner
        user = JobVyneUser.objects.create_user(
            self.data['owner_email'],
            first_name=self.data['owner_first_name'],
            last_name=self.data['owner_last_name'],
            user_type_bits=JobVyneUser.USER_TYPE_EMPLOYER,
            employer_id=employer.id,
            is_employer_owner=True
        )
        
        admin_group = EmployerAuthGroup.objects.get(employer_id=None, name='Admin')
        UserEmployerPermissionGroup(
            user=user,
            employer=employer,
            permission_group=admin_group,
            is_employer_approved=True
        )
        
        # Send password reset to owner
        # TODO: Look into sending welcome email instead of password reset
        UserView.send_password_reset_email(request, user.email, {
            'extra_email_context': {
                'supportEmail': EMAIL_ADDRESS_SUPPORT
            }
        })
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Employer successfully created'
        })
    
    @staticmethod
    def get_employers(employer_id=None, employer_filter=None):
        if employer_id:
            employer_filter = Q(id=employer_id)
            
        employers = Employer.objects \
            .filter(employer_filter)\
            .annotate(employee_count=Count('employee'))
        if employer_id:
            if not employers:
                raise Employer.DoesNotExist
            return employers[0]
        return employers
    
    @staticmethod
    def get_serialized_employer(employer: Employer):
        return {
            'id': employer.id,
            'name': employer.employer_name,
            'joined_date': get_datetime_format_or_none(employer.created_dt),
            'employee_count': employer.employee_count,
            'account_status': None,  # TODO: Based on payment history - active, past-due, cancelled
            'account_owner_name': None,  # TODO: Need to set mechanism for creating an account owner for each employer
            'account_owner_email': None
        }
