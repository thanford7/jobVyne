import json
from datetime import timedelta

import names
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.utils import timezone
from rest_framework.test import APIClient

from jvapp.models import *
from jvapp.models.user import StandardPermissionGroups
from jvapp.urls import api_path


class BaseTestCase(TestCase):
    REQUEST_GET = 'GET'
    REQUEST_POST = 'POST'
    REQUEST_PUT = 'PUT'
    DEFAULT_USER_PASSWORD = 'Super!Secure1'
    
    def setUp(self) -> None:
        call_command('collectstatic', '--noinput')
        self.client = APIClient()
        self.employer_permission_groups = {g.name: g for g in EmployerAuthGroup.objects.all()}
        self.permissions = {p.name: p for p in EmployerPermission.objects.all()}
        self.employer = self.create_employer('ChickFilet')
        self.user_admin = self.create_user(
            JobVyneUser.USER_TYPE_ADMIN, first_name='Billy', last_name='Jean'
        )
        self.user_employer_admin = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYER, first_name='Britney', last_name='Spears',
            employer_id=self.employer.id, auth_group_names=[StandardPermissionGroups.ADMIN.value]
        )
        
        # HR auth group is the default so we don't need to set it explicitly
        self.user_employer_hr = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYER, first_name='Scooby', last_name='Doo',
            employer_id=self.employer.id
        )
        self.user_employee = self.create_user(
            JobVyneUser.USER_TYPE_EMPLOYEE, first_name='Shark', last_name='Nado', employer_id=self.employer.id
        )
        self.user_candidate = self.create_user(
            JobVyneUser.USER_TYPE_CANDIDATE, first_name='Bobby', last_name='Dupree'
        )
        self.currency = Currency.objects.get(name='USD')
        self.job_departments = [self.create_job_department(name) for name in ['Software', 'Product', 'Marketing']]
        self.cities = [self.create_city(name) for name in ['Boston', 'Denver', 'Miami']]
        self.states = [self.create_state(name) for name in ['MA', 'CO', 'FL']]
        self.countries = list(Country.objects.all())
        self.locations = [self.create_location(*data) for data in [
            ('Boston, MA, US', self.cities[0], self.states[0], self.countries[0]),
            ('Denver, CO, US', self.cities[1], self.states[1], self.countries[0]),
            ('Miami, FL, US', self.cities[2], self.states[2], self.countries[0])
        ]]
        self.jobs = [self.create_job(data[0], **data[1]) for data in [
            (
                [self.locations[0], self.locations[2]],
                {
                    'employer': self.employer,
                    'job_title': 'Software Engineer - L1',
                    'job_department': self.job_departments[0],
                    'open_date': timezone.now().date() - timedelta(days=60),
                }
            ),
            (
                [self.locations[1]],
                {
                    'employer': self.employer,
                    'job_title': 'Software Engineer - L2',
                    'job_department': self.job_departments[0],
                    'open_date': timezone.now().date() - timedelta(days=30),
                }
            ),
            (
                [self.locations[0]],
                {
                    'employer': self.employer,
                    'job_title': 'Product Manager',
                    'job_department': self.job_departments[1],
                    'open_date': timezone.now().date() - timedelta(days=20),
                }
            ),
            (
                [self.locations[2]],
                {
                    'employer': self.employer,
                    'job_title': 'Product Manager',
                    'job_department': self.job_departments[1],
                    'open_date': timezone.now().date() - timedelta(days=40),
                }
            )
        ]]
        self.social_link = self.create_social_link(owner=self.user_employee)
    
    def make_get_request(self, url, data=None):
        return self._make_request(url, self.REQUEST_GET, data=data)
    
    def make_put_request(self, url, data=None, files=None):
        return self._make_request(url, self.REQUEST_PUT, data=data, files=files)
    
    def make_post_request(self, url, data=None, files=None):
        return self._make_request(url, self.REQUEST_POST, data=data, files=files)
    
    def _make_request(self, url, request_type, data=None, files=None):
        """
        :param url {str}:
        :param request_type {str}:
        :param data {dict}:
        :param files {list}: List of tuples (<file key>, <file>)
        :return: HttpResponse
        """
        url = f'/{api_path}{url}'
        
        if request_type == self.REQUEST_GET:
            return self.client.get(url, data)
        else:
            processed_data = {'data': json.dumps(data)}
            if files:
                for file_key, file in files:
                    processed_data[file_key] = file
            kwargs = {
                # This matches how data is processed and sent from the frontend
                'data': encode_multipart(data=processed_data, boundary=BOUNDARY),
                'content_type': MULTIPART_CONTENT
            }
            if request_type == self.REQUEST_POST:
                return self.client.post(url, **kwargs)
            elif request_type == self.REQUEST_PUT:
                return self.client.put(url, **kwargs)
    
    def create_employer(self, name):
        employer = Employer(employer_name=name)
        employer.save()
        return employer
    
    def create_employer_auth_group(self, name, user_type_bit, employer_id=None, is_default=False, permissions=None):
        employer_auth_group = EmployerAuthGroup(
            name=name,
            user_type_bit=user_type_bit,
            employer_id=employer_id,
            is_default=is_default
        )
        employer_auth_group.save()
        
        permissions = permissions or []
        for permission in permissions:
            employer_auth_group.permissions.add(permission)
        
        return employer_auth_group
    
    def create_user(self, user_type_bits, email=None, first_name=None, last_name=None, employer_id=None,
                    auth_group_names=None):
        first_name = first_name or names.get_first_name()
        last_name = last_name or names.get_last_name()
        email = email or f'{first_name}_{last_name}@jobvyne.com'
        user = JobVyneUser.objects.create_user(email, password=self.DEFAULT_USER_PASSWORD, **{
            'first_name': first_name,
            'last_name': last_name,
            'employer_id': employer_id,
            'user_type_bits': user_type_bits,
        })
        
        auth_group_names = auth_group_names or []
        for group_name in auth_group_names:
            auth_group = self.employer_permission_groups[group_name]
            UserEmployerPermissionGroup(
                user=user,
                employer_id=employer_id,
                permission_group=auth_group,
                is_employer_approved=True
            ).save()
        
        return user
    
    def create_currency(self, name, symbol):
        currency = Currency(name=name, symbol=symbol)
        currency.save()
        return currency
    
    def create_job_department(self, name):
        job_department = JobDepartment(name=name)
        job_department.save()
        return job_department
    
    def create_city(self, name):
        city = City(name=name)
        city.save()
        return city
    
    def create_state(self, name):
        state = State(name=name)
        state.save()
        return state
    
    def create_country(self, name):
        country = Country(name=name)
        country.save()
        return country
    
    def create_location(self, text, city, state, country):
        location = Location(text=text, city=city, state=state, country=country)
        location.save()
        return location
    
    def create_job(self, locations, **kwargs):
        job = EmployerJob(**kwargs)
        job.save()
        for location in locations:
            job.locations.add(location)
        return job
    
    def create_referral_bonus_rule(
            self, include_departments=None, exclude_departments=None,
            include_cities=None, exclude_cities=None,
            include_states=None, exclude_states=None,
            include_countries=None, exclude_countries=None,
            **kwargs
    ):
        rule = EmployerReferralBonusRule(**kwargs)
        rule.save()
        
        for dept in include_departments or []:
            rule.include_departments.add(dept)
        for dept in exclude_departments or []:
            rule.exclude_departments.add(dept)
        
        for city in include_cities or []:
            rule.include_cities.add(city)
        for city in exclude_cities or []:
            rule.exclude_cities.add(city)
        
        for state in include_states or []:
            rule.include_states.add(state)
        for state in exclude_states or []:
            rule.exclude_states.add(state)
        
        for country in include_countries or []:
            rule.include_countries.add(country)
        for country in exclude_countries or []:
            rule.exclude_countries.add(country)
        
        return rule
    
    def create_referral_bonus_rule_modifier(self, bonus_rule, **kwargs):
        modifier = EmployerReferralBonusRuleModifier(**kwargs)
        modifier.referral_bonus_rule = bonus_rule
        modifier.save()
        return modifier
    
    def create_social_link(self, owner, is_default=False, employer_id=None, cities=None, states=None, countries=None,
                           departments=None):
        social_link = SocialLinkFilter(
            is_default=is_default,
            owner=owner,
            employer_id=employer_id or owner.employer_id
        )
        social_link.save()
        
        if cities:
            for city in cities:
                social_link.cities.add(city)
        
        if states:
            for state in states:
                social_link.states.add(state)
        
        if countries:
            for country in countries:
                social_link.countries.add(country)
        
        if departments:
            for department in departments:
                social_link.departments.add(department)
        
        return social_link
    
    def login_user(self, user):
        resp = self.make_post_request('auth/login/', data={
            'email': user.email,
            'password': self.DEFAULT_USER_PASSWORD
        })
        if resp.status_code != 200:
            raise PermissionError('Unable to login user')
    
    def get_dummy_file(self, file_name, file_type='application/pdf'):
        return SimpleUploadedFile(file_name, b'Dummy file content', content_type=file_type)
    
    def assert_200_response(self, resp):
        self.assertEqual(200, resp.status_code)
