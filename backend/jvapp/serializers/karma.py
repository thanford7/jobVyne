from jvapp.models.karma import DonationOrganization, UserDonation
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_donation_organization(org: DonationOrganization):
    return {
        'id': org.id,
        'name': org.name,
        'logo_url': org.logo.url if org.logo else None,
        'url_main': org.url_main,
        'url_donation': org.url_donation
    }


def get_serialized_user_donation(donation: UserDonation, is_owner=False):
    data = {
        'id': donation.id,
        'user_name': donation.user.full_name,
        'donate_dt': get_datetime_format_or_none(donation.donate_dt),
        'donation_organization_id': donation.donation_organization.id,
        'donation_organization': get_serialized_donation_organization(donation.donation_organization),
        'donation_amount': donation.donation_amount,
        'donation_amount_currency': donation.donation_amount_currency.name
    }
    
    if is_owner:
        data['donation_receipt_url'] = donation.donation_receipt.url if donation.donation_receipt else None
    
    return data
