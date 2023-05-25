from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_error_response, get_success_response, get_warning_response
from jvapp.models import JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.karma import DonationOrganization, UserDonation, UserDonationOrganization, UserRequest
from jvapp.serializers.karma import get_serialized_donation_organization, get_serialized_user_donation, \
    get_serialized_user_request
from jvapp.utils.data import AttributeCfg, set_object_attributes


class DonationOrganizationView(JobVyneAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        organizations = DonationOrganization.objects.all()
        return Response(
            status=status.HTTP_200_OK,
            data=sorted([get_serialized_donation_organization(org) for org in organizations], key=lambda x: x['name'])
        )


class UserDonationOrganizationView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.query_params.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID is required')
        
        user_donation_organizations = self.get_user_donation_organizations(self.user, user_id)
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_donation_organization(udo.donation_organization) for udo in user_donation_organizations
        ])
    
    def post(self, request):
        user_donation_organization = UserDonationOrganization(
            user=self.user,
            donation_organization_id=self.data['donation_organization_id']
        )
        user_donation_organization.jv_check_permission(PermissionTypes.CREATE.value, self.user)
        try:
            user_donation_organization.save()
        except IntegrityError:
            return get_warning_response('You have already added this organization')
        
        return get_success_response('Added donation organization')

    @staticmethod
    def get_user_donation_organizations(user, user_id):
        user_donation_organizations = UserDonationOrganization.objects\
            .select_related('donation_organization')\
            .filter(user_id=user_id)
        return UserDonationOrganization.jv_filter_perm(user, user_donation_organizations)


class UserDonationView(JobVyneAPIView):
    
    def post(self, request):
        user_donation = UserDonation(user=self.user, donate_dt=timezone.now())
        self.update_user_donation(self.user, user_donation, self.data, self.files)
        return get_success_response('Added donation')
    
    @staticmethod
    def update_user_donation(user, user_donation, data, files):
        set_object_attributes(user_donation, data, {
            'donation_organization_id': None,
            'donation_amount': None,
            'donation_amount_currency_id': AttributeCfg(form_name='donation_amount_currency'),
            'donation_reason': None
        })
        if donation_receipt := files.get('donation_receipt'):
            user_donation.donation_receipt = donation_receipt[0]
        permission_type = PermissionTypes.CREATE.value if user_donation.id else PermissionTypes.EDIT.value
        user_donation.jv_check_permission(permission_type, user)
        user_donation.save()
        
        
class UserView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.data.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID is required')
        
        user = self.get_user(user_id)
        is_owner = user.id == self.user.id
        return Response(status=status.HTTP_200_OK, data={
            'user': {
                'name': user.full_name,
                'profile_picture_url': user.profile_picture.url if user.profile_picture else None
            },
            'donations': [get_serialized_user_donation(ud, is_owner=is_owner) for ud in user.donation.all()],
            'donation_organizations': [get_serialized_donation_organization(org) for org in user.donation_organization.all()]
        })
        
    @staticmethod
    def get_user(user_id):
        return JobVyneUser.objects\
            .prefetch_related(
                'donation_organization',
                'donation',
                'donation__donation_organization',
                'donation__donation_amount_currency'
            )\
            .get(id=user_id)


class UserRequestView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.query_params.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID is required')
        
        user_requests = self.get_user_requests(self.user, user_id)
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_user_request(ur) for ur in user_requests
        ])
    
    def post(self, request):
        if not (user_id := self.data.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID is required')
        
        request_type = self.data['request_type']
        user_request = UserRequest(user_id=user_id, request_type=request_type)
        self.update_user_request(self.user, user_request, self.data)
        return get_success_response(f'Created new {request_type} request')
        
    def put(self, request):
        if not (user_request_id := self.data.get('user_request_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user request ID is required')
        
        user_request = UserRequest.objects.get(id=user_request_id)
        self.update_user_request(self.user, user_request, self.data)
        return get_success_response('Updated request')
    
    @staticmethod
    def get_user_requests(user, user_id):
        user_requests = UserRequest.objects.filter(user_id=user_id)
        return UserRequest.jv_filter_perm(user, user_requests)

    @staticmethod
    def update_user_request(user, user_request, data):
        set_object_attributes(user_request, data, {
            'connection_first_name': AttributeCfg(is_ignore_excluded=True),
            'connection_last_name': AttributeCfg(is_ignore_excluded=True),
            'connection_linkedin_url': AttributeCfg(is_ignore_excluded=True),
            'connection_email': AttributeCfg(is_ignore_excluded=True),
            'connection_phone_number': AttributeCfg(is_ignore_excluded=True),
            'connector_first_name': AttributeCfg(is_ignore_excluded=True),
            'connector_last_name': AttributeCfg(is_ignore_excluded=True),
            'connector_email': AttributeCfg(is_ignore_excluded=True),
            'connector_phone_number': AttributeCfg(is_ignore_excluded=True),
        })
        
        permission_type = PermissionTypes.CREATE.value if user_request.id else PermissionTypes.EDIT.value
        user_request.jv_check_permission(permission_type, user)
        user_request.save()
        