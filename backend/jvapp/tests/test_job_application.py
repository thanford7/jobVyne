from jvapp.models import JobApplication
from jvapp.tests.base import BaseTestCase


class JobApplicationTestCase(BaseTestCase):
    
    def test_get_jobs_from_link(self):
        resp = self._make_request(f'social-link-jobs/{self.social_link.id}', self.REQUEST_GET, data={'page_count': 1})
        self.assert_200_response(resp)
        self.assertEqual(len(self.jobs), len(resp.data['jobs']))
        
    def test_submit_an_application_new_user(self):
        resume_file = self.get_dummy_file('resume.pdf')
        email = 'boggart1@hotmail.com'
        resp = self._make_request('job-application/', self.REQUEST_POST, data={
            'filter_id': str(self.social_link.id),
            'email': email,
            'job_id': self.jobs[0].id,
            'first_name': 'Humphrey',
            'last_name': 'Bogart',
            'phone_number': '202-917-2200',
            'linkedin_url': 'https://www.linkedin.com/boggart',
        }, files=[('resume', resume_file)])
        self.assert_200_response(resp)
        applications = JobApplication.objects.filter(email=email)
        self.assertEqual(1, len(applications))
        
    def test_submit_an_application_logged_in_user(self):
        self.login_user(self.user_candidate)
        resume_file = self.get_dummy_file('resume.pdf')
        email = 'boggart2@hotmail.com'
        resp = self._make_request('job-application/', self.REQUEST_POST, data={
            'filter_id': str(self.social_link.id),
            'email': email,
            'job_id': self.jobs[1].id,
            'first_name': 'Stanley',
            'last_name': 'Bogart'
        }, files=[('resume', resume_file)])
        self.assert_200_response(resp)
        applications = JobApplication.objects.filter(email=email)
        self.assertEqual(1, len(applications))
        