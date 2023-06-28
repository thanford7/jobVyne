from jvapp.models.user import JobVyneUser, StandardPermissionGroups
from jvapp.tests.base import BaseTestCase


class EmployerGroupPermissionsTestCase(BaseTestCase):
    
    def test_save_new_user(self):
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYEE, employer_id=self.employer.id)
        perm_groups = new_user_employer.employer_permission_group.all()
        
        # Expect the Django receiver to add a default permission group
        self.assertEqual(len(perm_groups), 1)
        
        # Default group for Employees is the Employee group
        self.assertEqual(perm_groups[0].permission_group_id, self.employer_permission_groups[StandardPermissionGroups.EMPLOYEE.value].id)
        
        # Create a new default for the EMPLOYEE user type
        new_auth_group = self.create_employer_auth_group(
            'Super employee', JobVyneUser.USER_TYPE_EMPLOYEE, employer_id=self.employer.id, is_default=True
        )

        # New employer users should now default to Super employee
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYEE, employer_id=self.employer.id)
        new_user_employer = JobVyneUser.objects.prefetch_related('employer_permission_group').get(id=new_user_employer.id)
        perm_groups = new_user_employer.employer_permission_group.all()
        self.assertEqual(perm_groups[0].permission_group_id, new_auth_group.id)
        
