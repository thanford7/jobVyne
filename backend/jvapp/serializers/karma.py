from jvapp.models.karma import DonationOrganization, UserDonation, UserRequest
from jvapp.serializers.employer import get_serialized_currency
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_donation_organization(org: DonationOrganization):
    return {
        'id': org.id,
        'ein': org.ein,
        'name': org.name,
        'logo_url': org.logo.url if org.logo else None,
        'url_main': org.url_main,
        'description': org.description
    }


def get_serialized_user_donation(donation: UserDonation, is_owner=False):
    data = {
        'id': donation.id,
        'user_name': donation.user.full_name,
        'donate_dt': get_datetime_format_or_none(donation.donate_dt),
        'donation_organization_id': donation.donation_organization.id,
        'donation_organization': get_serialized_donation_organization(donation.donation_organization),
        'donation_amount': donation.donation_amount,
        'donation_amount_currency': get_serialized_currency(donation.donation_amount_currency),
        'is_verified': donation.is_verified
    }
    
    if is_owner:
        data['donation_receipt_url'] = donation.donation_receipt.url if donation.donation_receipt else None
    
    return data


def get_serialized_user_request(user_request: UserRequest):
    return {
        'id': user_request.id,
        'request_type': user_request.request_type,
        'connection_first_name': user_request.connection_first_name,
        'connection_last_name': user_request.connection_last_name,
        'connection_linkedin_url': user_request.connection_linkedin_url,
        'connection_email': user_request.connection_email,
        'connection_phone_number': user_request.connection_phone_number,
        'connection_donation_org': get_serialized_donation_organization(user_request.connection_donation_org),
        'connector_first_name': user_request.connector_first_name,
        'connector_last_name': user_request.connector_last_name,
        'connector_email': user_request.connector_email,
        'connector_phone_number': user_request.connection_phone_number,
        'request_data': user_request.request_data
    }
