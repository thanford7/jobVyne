from django.core import mail

from jvapp.models import JobApplication
from jvapp.tests.base import BaseTestCase


class JobApplicationTestCase(BaseTestCase):
    
    def test_get_jobs_from_link(self):
        resp = self._make_request(f'social-link-jobs/{self.social_link.id}', self.REQUEST_GET, data={'page_count': 1})
        self.assert_200_response(resp)
        self.assertEqual(len(self.jobs), len(resp.data['jobs']))
        
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
        resp = self._submit_application('toodaloo@yahoo.com')
        self.assert_200_response(resp)
        # 3 new emails should have been sent. One for each - employer, candidate, referrer
        self.assertEqual(current_mail_count + 3, len(mail.outbox))
        
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