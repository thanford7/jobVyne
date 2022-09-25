from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

import stripe
from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models import Employer

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def get_price(price_in_pennies):
    if not price_in_pennies:
        return price_in_pennies
    return price_in_pennies / 100


class StripeCustomerView(JobVyneAPIView):
    
    def get(self, request):
        pass
    
    @staticmethod
    def get_customer(customer_key):
        return stripe.Customer.retrieve(customer_key)
    
    @staticmethod
    def create_or_update_customer(employer: Employer):
        update_data = {
            'name': employer.employer_name,
            'email': employer.billing_email,
            'address': {
                'line1': employer.street_address,
                'line2': employer.street_address_2,
                'city': employer.city,
                'state': employer.state,
                'country': employer.country,
                'postal_code': employer.postal_code
            },
            'metadata': {
                'employer_id': employer.id
            }
        }
        if employer.stripe_customer_key:
            stripe.Customer.modify(
                employer.stripe_customer_key,
                **update_data
            )
        else:
            customer = stripe.Customer.create(**update_data)
            employer.stripe_customer_key = customer['id']
            employer.save()


class StripeProductView(JobVyneAPIView):
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=self.get_products())
    
    @staticmethod
    def get_products():
        products = {
            product['id']: {
                'id': product['id'],
                'prices': [],
                'name': product['name']
            }
            for product in stripe.Product.list(active=True)['data']
        }
        prices = stripe.Price.list(active=True, expand=['data.tiers'])['data']
    
        for price in prices:
            product = products[price['product']]
            product['prices'].append({
                'id': price['id'],
                'billing_scheme': price['billing_scheme'],
                'currency': price['currency'],
                'interval': price['recurring']['interval'],
                'type': price['type'],
                'tiers': [{
                    'flat_amount': get_price(tier['flat_amount']),
                    'unit_amount': get_price(tier['unit_amount'])
                } for tier in price['tiers']]
            })
    
        return products
