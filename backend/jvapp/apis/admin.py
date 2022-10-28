import json

from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.apis.user import UserView
from jvapp.models import Employer, EmployerAuthGroup, JobVyneUser, UserEmployerPermissionGroup
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.permissions.general import IsAdmin
from jvapp.serializers.user import get_serialized_user
from jvapp.utils.data import AttributeCfg, coerce_bool, set_object_attributes
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


class AdminUserView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    
    def get(self, request):
        filters = json.loads(self.query_params['filters'])
        page_count = self.query_params['page_count']
        users = UserView.get_user(
            self.user, user_filter=Q(), is_check_permission=False,
        ).order_by(f'{"-" if coerce_bool(self.query_params["is_descending"]) else ""}{self.query_params.get("sort_order", "id")}')
        
        if employer_id := filters.get('employer_id'):
            users = users.filter(employer_id=employer_id)
        
        if not self.user.is_admin:
            if not employer_id:
                return Response('You must provide an employer ID', status=status.HTTP_400_BAD_REQUEST)
            if employer_id != self.user.employer_id:
                return Response('You do not have access to this employer', status=status.HTTP_401_UNAUTHORIZED)
        
        if search_text := filters.get('searchText'):
            search_filter = Q(first_name__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(last_name__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(email__iregex=f'^.*{search_text}.*$')
            search_filter |= Q(business_email__iregex=f'^.*{search_text}.*$')
            users = users.filter(search_filter)
        
        if user_type_bits_list := filters.get('userTypeBitsList'):
            user_type_bits = sum(user_type_bits_list)
            users = users.filter(user_type_bits__lt=F('user_type_bits') + (1 * F('user_type_bits').bitand(user_type_bits)))
            
        if permission_group_ids := filters.get('permissionGroupIds'):
            users = users.filter(employer_permission_group__permission_group_id__in=permission_group_ids)

        if is_approval_required := filters.get('isApprovalRequired'):
            users = users.filter(is_approval_required__in=is_approval_required)
            
        if is_active := filters.get('isActive'):
            is_not_active = [not x for x in is_active]
            users = users.filter(is_employer_deactivated__in=is_not_active)
            
        if has_employee_seat := filters.get('hasEmployeeSeat'):
            users = users.filter(has_employee_seat__in=has_employee_seat)
            
        paged_users = Paginator(users, per_page=25)
        data = {
            'total_page_count': paged_users.num_pages,
            'total_user_count': paged_users.count,
            'users': [get_serialized_user(user, is_include_employer_info=True, is_include_personal_info=True) for user in paged_users.get_page(page_count)]
        }
        
        return Response(status=status.HTTP_200_OK, data=data)
