from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_error_response, get_success_response, get_warning_response
from jvapp.apis.donation_org import DonationOrgView
from jvapp.models import JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.karma import DonationOrganization, UserDonation, UserDonationOrganization, UserRequest
from jvapp.serializers.karma import get_serialized_donation_organization, get_serialized_user_donation, \
    get_serialized_user_request
from jvapp.utils.data import AttributeCfg, set_object_attributes
from jvapp.utils.image import convert_url_to_image


class DonationOrganizationView(JobVyneAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        organizations = DonationOrganization.objects.all()
        return Response(
            status=status.HTTP_200_OK,
            data=sorted([get_serialized_donation_organization(org) for org in organizations], key=lambda x: x['name'])
        )
    
    @staticmethod
    def get_or_create_donation_org(ein):
        try:
            return DonationOrganization.objects.get(ein=ein)
        except DonationOrganization.DoesNotExist:
            return DonationOrganizationView.create_donation_org(ein)
    
    @staticmethod
    def create_donation_org(ein):
        donation_org_data = DonationOrgView.get_raw_donation_org(ein)
        donation_org = DonationOrganization()
        set_object_attributes(donation_org, donation_org_data, {
            'ein': None,
            'every_org_key': AttributeCfg(form_name='id'),
            'name': None,
            'url_main': AttributeCfg(form_name='profileUrl'),
            'description': None
        })
        donation_org.logo = convert_url_to_image(
            donation_org_data['logoUrl'], f'{donation_org_data["primarySlug"]}_logo'
        )
        donation_org.save()
        return donation_org
        

class UserDonationOrganizationView(JobVyneAPIView):
    
    def get(self, request):
        if not (user_id := self.query_params.get('user_id')):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID is required')
        
        user_donation_organizations = self.get_user_donation_organizations(self.user, user_id)
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_donation_organization(udo.donation_organization) for udo in user_donation_organizations
        ])
    
    def post(self, request):
        org_data = self.data.get('org')
        donation_org = DonationOrganizationView.get_or_create_donation_org(org_data['ein'])
        user_donation_organization = UserDonationOrganization(
            user=self.user,
            donation_organization_id=donation_org.id
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
    
    def get(self, request):
        user_id = self.query_params['user_id']
        user_donations = UserDonation.objects.filter(user_id=user_id)
        is_owner = self.user.id == user_id
        return Response(status=status.HTTP_200_OK, data=[
            get_serialized_user_donation(ud, is_owner=is_owner) for ud in user_donations
        ])
    
    def post(self, request):
        user_donation = UserDonation(user=self.user, donate_dt=timezone.now())
        self.update_user_donation(self.user, user_donation, self.data, self.files)
        return get_success_response('Added donation')
    
    def put(self, request):
        try:
            user_donation = UserDonation.objects.get(id=self.data['donation_id'])
        except UserDonation.DoesNotExist:
            return get_error_response('This donation does not exist')
        
        user_donation.is_verified = True
        user_donation.donate_dt = timezone.now()
        user_donation.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        user_donation.save()
        return get_success_response('Donation confirmed')
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        user_id = self.query_params.get('user_id')
        request_id = self.query_params.get('request_id')
        if not any((user_id, request_id)):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='A user ID or request ID is required')
        
        if request_id:
            user_request = self.get_user_requests(self.user, request_id=request_id)
            return Response(status=status.HTTP_200_OK, data={
                'user_request': get_serialized_user_request(user_request),
                'user': {
                    'first_name': user_request.user.first_name,
                    'last_name': user_request.user.last_name,
                    'email': user_request.user.email,
                    'linkedin_url': user_request.user.linkedin_url,
                    'profile_picture_url': user_request.user.profile_picture.url if user_request.user.profile_picture else None
                },
                'donation_organizations': [
                    get_serialized_donation_organization(user_org.donation_organization) for
                    user_org in user_request.user.donation_organization.all()
                ]
            })

        user_requests = self.get_user_requests(self.user, user_id=user_id)
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
    def get_user_requests(user, user_id=None, request_id=None):
        user_request_filter = Q()
        if request_id:
            user_request_filter = Q(id=request_id)
        elif user_id:
            user_request_filter = Q(user_id=user_id)
        user_requests = UserRequest.objects\
            .select_related('user', 'connection_donation_org')\
            .prefetch_related('user__donation_organization__donation_organization')\
            .filter(user_request_filter)
        
        # Don't apply user filter to single request. This will be access by a public page
        if request_id:
            if not user_requests:
                raise UserRequest.DoesNotExist
            return user_requests[0]

        user_requests = UserRequest.jv_filter_perm(user, user_requests)
        return user_requests

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
        
        
class UserRequestDonationOrgView(JobVyneAPIView):
    permission_classes = [AllowAny]
    
    def put(self, request):
        user_request = UserRequestView.get_user_requests(self.user, request_id=self.data['request_id'])
        donation_org = DonationOrganizationView.get_or_create_donation_org(self.data['ein'])
        user_request.connection_donation_org = donation_org
        user_request.save()
        return get_success_response('Updated donation organization')
