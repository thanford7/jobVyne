from io import StringIO

from jvapp import models
from jvapp.tests.base import BaseTestCase
from jvapp.utils import csv


class CsvUploadTest(BaseTestCase):
    def test_csv(self):
        employer = models.Employer.objects.filter(employer_name='ChickFilet').first()
        self.assertEqual(0, models.JobVyneUser.objects.filter(email='michael@jobvyne.com').count())
        csv_text = '\n'.join([
            "email,first_name,last_name,user_type_bits,phone",
            "mark@jobvyne.com,Marky,  Mark,1,(610)585-2457",
        ])
        with StringIO(csv_text) as csv_file:
            csv.bulk_load_users(csv_file, employer)
        user = models.JobVyneUser.objects.get(email='mark@jobvyne.com')
        initial_id = user.id
        self.assertEqual('Marky', user.first_name)
        self.assertEqual('Mark', user.last_name)
        self.assertEqual('(610)585-2457', user.phone_number)
        self.assertEqual(models.JobVyneUser.USER_TYPE_EMPLOYEE, user.user_type_bits)
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
        self.assertEqual('(610)585-2457', user.phone_number)
        self.assertEqual(employer, user.employer)
        self.assertEqual(initial_id, user.id)
        # Make sure the mod time has been updated via save signals
        self.assertGreater(user.modified_dt, initial_mod_time)

    def test_validate_email(self):
        employer = models.Employer.objects.filter(employer_name='ChickFilet').first()
        # Make sure the email domain rules are followed when an employer has email domains set
        employer.email_domains = 'chickfilet.com'
        employer.save()
        csv_text = '\n'.join([
            "email,first,last",
            "employee@chickfilet.com,Workhere,Truly",
            "nonemployee@chickfilb.com,Donut,Workhere",
        ])
        with StringIO(csv_text) as csv_file:
            csv.bulk_load_users(csv_file, employer)
        # NEITHER of the two employees shall have been added
        users = models.JobVyneUser.objects.filter(email__in=['employee@chickfilet.com', 'nonemployee@chickfilb.com'])
        self.assertFalse(users.exists())

        csv_text = '\n'.join([
            "email,first,last",
            "employee@chickfilet.com,Workhere,Truly",
        ])
        with StringIO(csv_text) as csv_file:
            csv.bulk_load_users(csv_file, employer)
        # The employee shall have been added
        users = models.JobVyneUser.objects.filter(email='employee@chickfilet.com')
        self.assertEqual(1, users.count())

