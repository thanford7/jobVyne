import json
from datetime import timedelta

from django.core import mail
from django.db.models import Q
from django.utils import timezone

from jvapp.apis.notification import BaseMessageView
from jvapp.models.employer import EmployerJob
from jvapp.models.job_seeker import JobApplication
from jvapp.models.location import REMOTE_TYPES
from jvapp.models.tracking import MessageGroup
from jvapp.tests.base import BaseTestCase


class JobApplicationTestCase(BaseTestCase):
    
    def test_get_jobs_from_link(self):
        # Make sure we return all jobs
        job_infos = self._get_jobs_from_social_link(page_count=1)
        self.assertEqual(len(self.jobs), len(job_infos))
    
    def test_get_jobs_from_social_link(self):
        search_title = 'Engineer'
        job_infos = self._get_jobs_from_social_link(search_regex=search_title)
        self.assertLess(len(job_infos), len(self.jobs))
        for job_info in job_infos:
            self.assertTrue(search_title in job_info['job_title'])
    
    def test_get_jobs_from_link_near(self):
        def job_has_location_part(job_info, location_parts, location_part_key):
            for location in job_info['locations']:
                if location[location_part_key] in location_parts:
                    return True
            return False
        
        base_job_data = {
            'employer': self.employer,
            'job_title': 'Tortoise Trainer',
            'job_department': self.job_departments[1],
            'open_date': timezone.now().date() - timedelta(days=40),
        }
        location_remote_us = self.create_location(
            'Remote: United States', None, None, self.countries[0], 35.6658404,
            -116.930071, is_remote=True
        )
        self.create_job([location_remote_us], **base_job_data)
        location_remote_california = self.create_location(
            'Remote: CA', None, self.create_state('CA'), self.countries[0],
            37.1515743, -124.5923051, is_remote=True
        )
        self.create_job([location_remote_california], **base_job_data)
        location_remote_france = self.create_location(
            'Remote: France', None, None, self.countries[1], 46.0975255, -3.2288209,
            is_remote=True
        )
        self.create_job([location_remote_france], **base_job_data)
        location_global_remote = self.create_location('Remote', None, None, None, None, None, is_remote=True)
        self.create_job([location_global_remote], **base_job_data)
        
        location_search_with_city = {
            'text': 'Boston, MA, USA 02109',
            'city': 'Boston',
            'state': 'MA',
            'country': 'USA',
            'postal_code': '02109',
            'latitude': 42.314232,
            'longitude': -71.1350906
        }
        
        location_search_without_city = {
            'text': 'CA, USA 02109',
            'city': None,
            'state': 'CA',
            'country': 'USA',
            'postal_code': None,
            'latitude': 37.1515743,
            'longitude': -124.5923051
        }
        
        # Within 5 miles of 02109 we should just get the Boston jobs
        job_infos = self._get_jobs_from_social_link(location=json.dumps(location_search_with_city), range_miles=5)
        self.assertEqual(2, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_location_part(job_info, ('Boston',), 'city'))
        
        # Within 50 miles, we should also get the Newton job
        job_infos = self._get_jobs_from_social_link(location=json.dumps(location_search_with_city), range_miles=50)
        self.assertEqual(3, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_location_part(job_info, ('Boston', 'Newton'), 'city'))
            
        # Filter on state
        job_infos = self._get_jobs_from_social_link(location=json.dumps(location_search_without_city))
        jobs_in_ca_count = EmployerJob.objects\
            .filter(locations__state__name=location_search_without_city['state']).count()
        self.assertEqual(jobs_in_ca_count, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_location_part(job_info, ('CA',), 'state'))
            
        # Filter on all remote jobs
        job_infos = self._get_jobs_from_social_link(remote_type_bit=REMOTE_TYPES.YES.value)
        jobs_remote_count = EmployerJob.objects\
            .filter(locations__is_remote=True).count()
        self.assertEqual(jobs_remote_count, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_location_part(job_info, (True,), 'is_remote'))
            
        # Filter on US remote jobs
        job_infos = self._get_jobs_from_social_link(
            location=json.dumps(location_search_without_city),
            remote_type_bit=REMOTE_TYPES.YES.value
        )
        location_filter = Q(locations__country__name='USA') | Q(locations__country__isnull=True)
        jobs_remote_us_count = EmployerJob.objects \
            .filter(locations__is_remote=True).filter(location_filter).count()
        self.assertEqual(jobs_remote_us_count, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_location_part(job_info, (True,), 'is_remote'))
            self.assertTrue(job_has_location_part(job_info, ('USA', None), 'country'))
    
    def test_submit_an_application_new_user(self):
        email = 'boggart1@hotmail.com'
        resp = self._submit_application(
            email, phone_number='202-917-2200', linkedin_url='https://www.linkedin.com/boggart'
        )
        self.assert_200_response(resp)
        applications = JobApplication.objects.filter(email=email)
        self.assertEqual(1, len(applications))
    
    def test_submit_an_application_logged_in_user(self):
        self.login_user(self.user_candidate)
        email = 'boggart2@hotmail.com'
        resp = self._submit_application(email)
        self.assert_200_response(resp)
        applications = JobApplication.objects.filter(email=email)
        self.assertEqual(1, len(applications))
    
    def test_email_notifications(self):
        # Adding a notification email will make all future applications trigger an email to the employer
        self.employer.notification_email = 'bogus@jobvyne.com'
        self.employer.save()
        current_mail_count = len(mail.outbox)
        current_message_thread_count = self._get_message_thread_count()
        resp = self._submit_application('toodaloo@yahoo.com')
        self.assert_200_response(resp)
        
        # 3 new emails should have been sent. One for each - employer, candidate, referrer
        self.assertEqual(current_mail_count + 3, len(mail.outbox))
        
        # A new message thread should have been started for this application
        self.assertEqual(current_message_thread_count + 1, self._get_message_thread_count())
        
        # A new employer group should have been created to track all message threads related to this employer
        self.assertEqual(1, self._get_message_group_count())
        
        # Send another email and make sure another message group is NOT created. We should use the group that
        # was just created
        resp = self._submit_application('toodaloo2@yahoo.com')
        self.assert_200_response(resp)
        self.assertEqual(1, self._get_message_group_count())
    
    def _get_message_thread_count(self):
        return BaseMessageView.get_message_threads(Q(message_groups__employer=self.employer)).count()
    
    def _get_message_group_count(self):
        return MessageGroup.objects.filter(employer=self.employer).count()
    
    def _submit_application(self, email, phone_number=None, linkedin_url=None):
        resume_file = self.get_dummy_file('resume.pdf')
        return self._make_request('job-application/', self.REQUEST_POST, data={
            'filter_id': str(self.social_link.id),
            'email': email,
            'job_id': self.jobs[0].id,
            'first_name': 'Humphrey',
            'last_name': 'Bogart',
            'phone_number': phone_number,
            'linkedin_url': linkedin_url,
        }, files=[('resume', resume_file)])
    
    def _get_jobs_from_social_link(self, **data_kwargs):
        resp = self.make_get_request(f'social-link-jobs/{self.social_link.id}', data=dict(**data_kwargs))
        self.assert_200_response(resp)
        return resp.data['jobs']
