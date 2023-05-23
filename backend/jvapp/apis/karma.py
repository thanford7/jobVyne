from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_error_response, get_success_response, get_warning_response
from jvapp.models import JobVyneUser
from jvapp.models.abstract import PermissionTypes
from jvapp.models.karma import DonationOrganization, UserDonation, UserDonationOrganization
from jvapp.serializers.karma import get_serialized_donation_organization, get_serialized_user_donation
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
