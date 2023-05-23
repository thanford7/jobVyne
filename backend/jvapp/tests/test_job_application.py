from unittest.mock import patch

from django.core import mail
from django.db.models import Q

from jvapp.apis.notification import BaseMessageView
from jvapp.models import JobApplication
from jvapp.models.tracking import MessageGroup
from jvapp.tests.base import BaseTestCase


class JobApplicationTestCase(BaseTestCase):
    
    def test_get_jobs_from_link(self):
        job_infos = self._get_jobs_from_social_link(page_count=1)
        self.assertEqual(len(self.jobs), len(job_infos))

    def test_get_jobs_from_link_filter(self):
        search_title = 'Engineer'
        job_infos = self._get_jobs_from_social_link(job_title=search_title)
        self.assertLess(len(job_infos), len(self.jobs))
        for job_info in job_infos:
            self.assertTrue(search_title in job_info['job_title'])

    @patch('jvapp.apis.geocoding.LocationParser.get_raw_location')
    def test_get_jobs_from_link_near(self, grl_mock):
        grl_mock.return_value = {
            'postal_code': '02109',
            'city': 'Boston',
            'state': 'Massachusetts',
            'country': 'United States',
            'country_short': 'US',
            'latitude': 42.36606159999999,
            'longitude': -71.0482911
        }
        def job_has_city(job_info, cities):
            for location in job_info['locations']:
                if location['city'] in cities:
                    return True
            return False
        # Within 5 miles of 02109 we should just get the Boston jobs
        job_infos = self._get_jobs_from_social_link(location='02109', range_miles=5)
        self.assertEqual(2, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_city(job_info, ('Boston',)))
        # Within 50 miles, we should also get the Newton job
        job_infos = self._get_jobs_from_social_link(location='02109', range_miles=50)
        self.assertEqual(3, len(job_infos))
        for job_info in job_infos:
            self.assertTrue(job_has_city(job_info, ('Boston', 'Newton')))


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

    def _get_jobs_from_social_link(self, **dataKwargs):
        resp = self.make_get_request(f'social-link-jobs/{self.social_link.id}', data=dict(**dataKwargs))
        self.assert_200_response(resp)
        job_dicts = []
        for employer_info in resp.data['jobs_by_employer']:
            for job_list in employer_info['jobs'].values():
                for job_info in job_list:
                    job_dicts.append(job_info)
        return job_dicts
