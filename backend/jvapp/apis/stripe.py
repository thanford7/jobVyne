from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import stripe
from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import Employer, EmployerSubscription, PermissionName
from jvapp.models.abstract import PermissionTypes
from jvapp.permissions.employer import IsAdminOrEmployerPermission
from jvapp.utils.datetime import get_datetime_from_unix
from jvapp.utils.email import EMAIL_ADDRESS_SUPPORT, send_email

stripe.api_key = settings.STRIPE_PRIVATE_KEY
ACCEPTED_PAYMENT_TYPES = ['card', 'us_bank_account']


def get_price(price_in_pennies):
    if not price_in_pennies:
        return price_in_pennies
    return int(price_in_pennies) / 100


class StripeBaseView(JobVyneAPIView):
    permission_classes = [IsAdminOrEmployerPermission]
    billing_permission = PermissionName.MANAGE_BILLING_SETTINGS.value
    
    def check_employer_permissions(self, customer_id=None, employer_id=None):
        if not any([customer_id, employer_id]):
            raise ValueError('A customer ID or employer ID is required')
        employer_filter = Q(id=employer_id) if employer_id else Q(stripe_customer_key=customer_id)
        employer = Employer.objects.prefetch_related('subscription').get(employer_filter)
        employer.jv_check_permission(PermissionTypes.EDIT.value, self.user)
        has_billing_permission = self.user.has_employer_permission(self.billing_permission, employer.id)
        if not has_billing_permission:
            raise PermissionError('You do not have permission to view billing settings')
        
        return employer


class StripeCustomerView(JobVyneAPIView):
    
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
            
            
class StripePaymentMethodView(StripeBaseView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer = self.check_employer_permissions(employer_id=employer_id)
        if not employer.stripe_customer_key:
            return Response(status=status.HTTP_200_OK)
        customer = StripeCustomerView.get_customer(employer.stripe_customer_key)
        payment_methods = []
        for payment_type in ACCEPTED_PAYMENT_TYPES:
            payments = stripe.Customer.list_payment_methods(
                employer.stripe_customer_key,
                type=payment_type,
            )
            if payments:
                for payment in payments:
                    payment_methods.append(self.normalize_payment_method(payment, customer.invoice_settings.default_payment_method))
        
        return Response(status=status.HTTP_200_OK, data=payment_methods)
    
    def put(self, request):
        if not (payment_method_id := self.data.get('id')):
            return Response('A payment method ID is required', status=status.HTTP_400_BAD_REQUEST)

        payment_method = stripe.PaymentMethod.retrieve(payment_method_id, expand=['customer'])
        self.check_employer_permissions(customer_id=payment_method.customer.id)
        
        if self.data.get('is_default'):
            stripe.Customer.modify(
                payment_method.customer.id,
                invoice_settings={"default_payment_method": payment_method_id},
            )
            
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully updated default payment method'
        })
        
    def delete(self, request, payment_method_id):
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id, expand=['customer'])
        self.check_employer_permissions(customer_id=payment_method.customer.id)
        
        if payment_method_id == payment_method.customer.invoice_settings.default_payment_method:
            return Response('You cannot delete the default payment method', status=status.HTTP_400_BAD_REQUEST)

        stripe.PaymentMethod.detach(payment_method_id)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully deleted payment method'
        })
    
    @staticmethod
    def normalize_payment_method(payment_method, default_payment_id):
        payment_type = payment_method['type']
        details = payment_method[payment_type]
        if payment_type == 'card':
            data = {
                'institution': details.brand,
                'exp_month': details.exp_month,
                'exp_year': details.exp_year,
                'last4': details.last4
            }
        elif payment_type == 'us_bank_account':
            data = {
                'institution': details.bank_name,
                'account_type': details.account_type,
                'last4': details.last4
            }
        else:
            raise ValueError(f'Unknown payment type: {payment_type}')
        
        data['id'] = payment_method.id
        data['type'] = payment_type
        data['is_default'] = default_payment_id and default_payment_id == payment_method.id
        return data
    
    
class StripeChargeView(StripeBaseView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
    
        employer = self.check_employer_permissions(employer_id=employer_id)
        charges = []
        if employer.stripe_customer_key:
            charges = stripe.Charge.list(customer=employer.stripe_customer_key, expand=['data.invoice', 'data.invoice.subscription'])['data']
        return Response(status=status.HTTP_200_OK, data=[self.normalize_charge(c) for c in charges])

    @staticmethod
    def normalize_charge(charge):
        return {
            'charge_amount': get_price(charge.amount),
            'charge_status': charge.status,
            'charge_dt': get_datetime_from_unix(charge.created),
            'receipt_url': charge.receipt_url,
            'failure_code': charge.failure_code,
            'failure_message': charge.failure_message,
            'period_start': get_datetime_from_unix(charge.invoice.subscription.current_period_start),
            'period_end': get_datetime_from_unix(charge.invoice.subscription.current_period_end),
            'invoice_pdf_url': charge.invoice.invoice_pdf
        }
    
    
class StripeInvoiceView(StripeBaseView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer = self.check_employer_permissions(employer_id=employer_id)
        invoices = stripe.Invoice.list(customer=employer.stripe_customer_key, status='paid', expand=['data.subscription'])['data']
        return Response(status=status.HTTP_200_OK, data=[self.normalize_invoice(i) for i in invoices])
    
    @staticmethod
    def normalize_invoice(invoice):
        return {
            'period_start': get_datetime_from_unix(invoice.subscription.current_period_start),
            'period_end': get_datetime_from_unix(invoice.subscription.current_period_end),
            'total_amount': get_price(invoice.total),
            'total_paid': get_price(invoice.amount_paid),
            'invoice_pdf_url': invoice.invoice_pdf
        }
    
    
class StripePayInvoiceView(StripeBaseView):
    
    def post(self, request):
        if not (payment_method_id := self.data.get('payment_method_id')):
            return Response('A payment method ID is required', status=status.HTTP_400_BAD_REQUEST)
        if not (invoice_id := self.data.get('invoice_id')):
            return Response('An invoice ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id, expand=['customer'])
        self.check_employer_permissions(customer_id=payment_method.customer.id)

        stripe.Invoice.pay(invoice_id, payment_method=payment_method_id)
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Payment processed successfully'
        })


class StripeProductView(JobVyneAPIView):
    # This is the number of employee seats where pricing tiers should end
    # Above this number, we will develop a custom price proposal for the customer
    MAX_PRODUCT_COUNT = 1000
    
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
                'tiers': StripeProductView.get_price_tiers(price['tiers'])
            })
        
        return list(products.values())
    
    @staticmethod
    def get_price_tiers(raw_tiers):
        tiers = []
        lower_count = 0
        for tier in raw_tiers:
            tiers.append({
                'flat_amount': get_price(tier['flat_amount']),
                'unit_amount': get_price(tier['unit_amount']),
                'lower_count': lower_count + 1,
                'upper_count': tier['up_to'] or StripeProductView.MAX_PRODUCT_COUNT
            })
            lower_count = tier['up_to']
        
        return tiers


class StripeSubscriptionView(StripeBaseView):
    
    def get(self, request):
        from jvapp.apis.employer import EmployerSubscriptionView  # Avoid circular import
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer = self.check_employer_permissions(employer_id=employer_id)
        jv_subscription = EmployerSubscriptionView.get_subscription(employer)
        if not jv_subscription:
            subscription_data = None
        elif not jv_subscription.stripe_key:
            subscription_data = {
                'active': jv_subscription.status == 'active',
                'interval': 'year',
                'quantity': jv_subscription.employee_seats,
                'total_price': 0,
                'status': jv_subscription.status
            }
        else:
            subscription = stripe.Subscription.retrieve(
                jv_subscription.stripe_key,
                expand=['latest_invoice', 'latest_invoice.payment_intent']
            )
            subscription_item = subscription.to_dict()['items']['data'][0]
            subscription_price = subscription_item['price']
            unit_price = get_price(subscription.latest_invoice.lines.data[0]['unit_amount_excluding_tax'])
            subscription_data = {
                'id': subscription.id,
                'active': subscription_price['active'],
                'interval': subscription_price['recurring']['interval'],
                'quantity': subscription_item['quantity'],
                'latest_invoice': subscription.latest_invoice,
                'total_price': unit_price * subscription_item['quantity'],
                'start_date': datetime.fromtimestamp(subscription.current_period_start),
                'end_date': datetime.fromtimestamp(subscription.current_period_end),
                'is_cancel_at_end': subscription.cancel_at_period_end,
                'status': subscription.status
            }
        return Response(status=status.HTTP_200_OK, data=subscription_data)
    
    def post(self, request):
        from jvapp.apis.employer import EmployerSubscriptionView  # Avoid circular import
        employer = self.check_employer_permissions(employer_id=self.data['employer_id'])
        jv_subscription = EmployerSubscriptionView.get_subscription(employer)
        active_employees = EmployerSubscriptionView.get_active_employees(employer)
        
        if self.data['quantity'] < active_employees:
            return Response(
                f'The subscription seats of {self.data["quantity"]} is insufficient for the current {active_employees} active employees',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if jv_subscription:  # Update subscription if there is an active one
            subscription = stripe.Subscription.retrieve(jv_subscription.stripe_key)
            subscription_item = subscription.to_dict()['items']['data'][0]
            subscription_item = stripe.SubscriptionItem.modify(
                subscription_item.id,
                price=self.data['price_id'],
                quantity=self.data['quantity'],
                proration_behavior='always_invoice'
            )
            jv_subscription.employee_seats = self.data['quantity']
            jv_subscription.save()
        else:  # Create new subscription
            subscription = stripe.Subscription.create(
                items=[
                    {'price': self.data['price_id'], 'quantity': self.data['quantity']},
                ],
                customer=employer.stripe_customer_key,
                cancel_at_period_end=False,
                currency='USD',
                payment_behavior='default_incomplete',
                collection_method='charge_automatically',
            )
            
            EmployerSubscription(
                employer=employer,
                stripe_key=subscription.id,
                status=subscription.status,
                employee_seats=self.data['quantity']
            ).save()
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'JobVyne plan successfully updated'
        })
    
    def put(self, request, subscription_id):
        self.check_employer_permissions(employer_id=self.data['employer_id'])
        
        if self.data.get('is_reinstate'):
            subscription = stripe.Subscription.modify(subscription_id, cancel_at_period_end=False)
            jv_subscription = EmployerSubscription.objects.get(stripe_key=subscription.id)
            jv_subscription.status = subscription.status
            jv_subscription.save()
    
            return Response(status=status.HTTP_200_OK, data={
                SUCCESS_MESSAGE_KEY: 'Successfully un-cancelled subscription'
            })
        
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, subscription_id):
        employer = self.check_employer_permissions(employer_id=self.data['employer_id'])
        
        send_email('JobVyne | Customer cancellation', EMAIL_ADDRESS_SUPPORT, html_content=f'''
            <div>{employer.employer_name} (ID={employer.id}) cancelled their subscription</div>
        ''')

        subscription = stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
        jv_subscription = EmployerSubscription.objects.get(stripe_key=subscription.id)
        jv_subscription.status = subscription.status
        jv_subscription.save()
        
        return Response(status=status.HTTP_200_OK, data={
            SUCCESS_MESSAGE_KEY: 'Successfully cancelled subscription'
        })
    
    
class StripeSetupIntentView(StripeBaseView):
    
    def get(self, request):
        if not (employer_id := self.query_params.get('employer_id')):
            return Response('An employer ID is required', status=status.HTTP_400_BAD_REQUEST)
        
        employer = self.check_employer_permissions(employer_id=employer_id)
        
        # Check for existing setup intent and provide that instead of creating a new one
        setup_intents = stripe.SetupIntent.list(customer=employer.stripe_customer_key)
        setup_intent = next((s for s in setup_intents if s.status == 'requires_payment_method'), None)
        
        if not setup_intent:
            setup_intent = stripe.SetupIntent.create(
                customer=employer.stripe_customer_key,
                payment_method_types=ACCEPTED_PAYMENT_TYPES,
                usage='off_session'
            )
            
        return Response(status=status.HTTP_200_OK, data={'client_secret': setup_intent.client_secret})
        

class StripeWebhooksView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        # If you are testing your webhook locally with the Stripe CLI you
        # can find the endpoint's secret by running `stripe listen`
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(
                request.body, sig_header, settings.STRIPE_WEBHOOK_PRIVATE_KEY
            )
        except ValueError as e:
            raise e
        except stripe.error.SignatureVerificationError as e:
            raise e
            
            # Handle the event
        if event['type'] in ('customer.subscription.updated', 'customer.subscription.deleted'):
            # No need to handle 'customer.subscription.created' event because we update
            # The subscription status when we make the API call
            subscription = event['data']['object']
            jv_subscription = EmployerSubscription.objects.get(stripe_key=subscription.id)
            jv_subscription.status = subscription.status
            jv_subscription.save()
        elif event['type'] == 'invoice.created':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.deleted':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.finalization_failed':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.finalized':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.marked_uncollectible':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.paid':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.payment_action_required':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.payment_failed':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.payment_succeeded':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.sent':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.upcoming':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.updated':
            invoice = event['data']['object']
        elif event['type'] == 'invoice.voided':
            invoice = event['data']['object']
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            self.update_payment_method(payment_intent.customer, payment_intent.payment_method)
        elif event['type'] == 'setup_intent.succeeded':
            setup_intent = event['data']['object']
            self.update_payment_method(setup_intent.customer, setup_intent.payment_method)
        else:
            print('Unhandled event type {}'.format(event['type']))
        
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def update_payment_method(customer_id, payment_method):
        customer = stripe.Customer.retrieve(customer_id)
        # If no payment is attached to customer, make it the default
        if not customer.invoice_settings.default_payment_method:
            stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": payment_method},
            )
        else:
            stripe.PaymentMethod.attach(
                payment_method,
                customer=customer_id,
            )
