from jvapp.models import JobVyneUser
from jvapp.tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    
    def test_duplicate_user(self):
        self.user_admin.business_email = self.user_employee.email
        
        # This should fail since the email is already taken
        is_failed = self.is_failed(self.user_admin.save, ValueError)
        self.assertTrue(is_failed)
        
        new_email = 'gwen@hotmail.com'
        self.user_admin.business_email = new_email
        self.user_admin.save()

        # This should fail since the email is already taken
        is_failed = self.is_failed(
            lambda: self.create_user(
                JobVyneUser.USER_TYPE_CANDIDATE,
                first_name='Jackie', last_name='Jackson', email=new_email
            ),
            ValueError
        )
        self.assertTrue(is_failed)
        