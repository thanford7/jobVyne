from io import StringIO

from jvapp import models
from jvapp.tests.base import BaseTestCase
from jvapp.utils import csv


class JobApplicationTestCase(BaseTestCase):
    def test_simple(self):
        employer = models.Employer.objects.filter().first()
        self.assertEqual(0, models.JobVyneUser.objects.filter(email='michael@jobvyne.com').count())
        csv_text = '\n'.join([
            "email,first_name,last_name",
            "mark@jobvyne.com,Marky,Mark",
        ])
        with StringIO(csv_text) as csv_file:
            csv.bulk_load_users(csv_file, employer)
        user = models.JobVyneUser.objects.get(email='mark@jobvyne.com')
        initial_id = user.id
        self.assertEqual('Marky', user.first_name)
        self.assertEqual('Mark', user.last_name)
        self.assertEqual(employer, user.employer)
        initial_mod_time = user.modified_dt

        csv_text = '\n'.join([
            "email,first,last",
            "mark@jobvyne.com,Mark,Wahlberg",
        ])
        with StringIO(csv_text) as csv_file:
            csv.bulk_load_users(csv_file, employer)
        user = models.JobVyneUser.objects.get(email='mark@jobvyne.com')
        self.assertEqual('Mark', user.first_name)
        self.assertEqual('Wahlberg', user.last_name)
        self.assertEqual(employer, user.employer)
        self.assertEqual(initial_id, user.id)
        # Make sure the mod time has been updated via save signals
        self.assertGreater(user.modified_dt, initial_mod_time)
