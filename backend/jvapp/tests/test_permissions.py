from jvapp.models import JobVyneUser
from jvapp.models.user import DefaultPermissionGroups
from jvapp.tests.base import BaseTestCase


class EmployerGroupPermissionsTestCase(BaseTestCase):
    
    def test_save_new_user(self):
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYER, employer_id=self.employer.id)
        perm_groups = new_user_employer.permission_groups.all()
        
        # Expect the Django receiver to add a default permission group
        self.assertEqual(len(perm_groups), 1)
        
        # Default group for employers is the HR group
        self.assertEqual(perm_groups[0].id, self.employer_permission_groups[DefaultPermissionGroups.HR.value].id)
        
        # Create a new default for the EMPLOYER user type
        new_auth_group = self.create_employer_auth_group(
            'Finance', JobVyneUser.USER_TYPE_EMPLOYER, employer_id=self.employer.id, is_default=True
        )

        # New employer users should now default to finance
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYER, employer_id=self.employer.id)
        new_user_employer = JobVyneUser.objects.prefetch_related('permission_groups').get(id=new_user_employer.id)
        perm_groups = new_user_employer.permission_groups.all()
        self.assertEqual(perm_groups[0].id, new_auth_group.id)
    
    def test_add_user_to_new_group(self):
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYER, employer_id=self.employer.id)
        new_user_employer.permission_groups.add(self.employer_permission_groups[DefaultPermissionGroups.EMPLOYEE.value])
        
        # Adding the user to the Employee permission group should update their user type
        self.assertEqual(new_user_employer.user_type_bits, JobVyneUser.USER_TYPE_EMPLOYER | JobVyneUser.USER_TYPE_EMPLOYEE)
        
    def test_update_users_on_group_update(self):
        new_user_employer = self.create_user(JobVyneUser.USER_TYPE_EMPLOYER, employer_id=self.employer.id)
        super_influencer_group = self.create_employer_auth_group(
            'Super Influencer', JobVyneUser.USER_TYPE_INFLUENCER
        )
        new_user_employer.permission_groups.add(super_influencer_group)
        self.assertEqual(
            JobVyneUser.USER_TYPE_INFLUENCER,
            new_user_employer.user_type_bits & JobVyneUser.USER_TYPE_INFLUENCER
        )
        
        super_influencer_group.user_type_bit = JobVyneUser.USER_TYPE_EMPLOYEE
        super_influencer_group.save()
        
        # Refetch to get model updates
        new_user_employer = JobVyneUser.objects.get(id=new_user_employer.id)
        
        # Influencer type should be removed because the influencer group is now an employee type
        self.assertEqual(0, new_user_employer.user_type_bits & JobVyneUser.USER_TYPE_INFLUENCER)
        self.assertEqual(
            JobVyneUser.USER_TYPE_EMPLOYEE,
            new_user_employer.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYEE
        )
        
        # Employee user type should be removed when influencer group is deleted
        super_influencer_group.delete()

        # Refetch to get model updates
        new_user_employer = JobVyneUser.objects.get(id=new_user_employer.id)
        self.assertEqual(0, new_user_employer.user_type_bits & JobVyneUser.USER_TYPE_EMPLOYEE)
