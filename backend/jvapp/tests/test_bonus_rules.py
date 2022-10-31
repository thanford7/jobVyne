from jvapp.models import EmployerReferralBonusRuleModifier
from jvapp.serializers.employer import get_serialized_employer_job
from jvapp.tests.base import BaseTestCase


class ReferralBonusRulesTestCase(BaseTestCase):
    
    def get_serialized_jobs(self, jobs, rules):
        return [get_serialized_employer_job(job, rules=rules, is_include_bonus=True) for job in jobs]
    
    def test_add_bonus_rule(self):
        # Create a new rule for software jobs
        new_rule = self.create_referral_bonus_rule(
            include_departments=[self.job_departments[0]],
            employer=self.employer,
            order_idx=0,
            base_bonus_amount=1000,
            bonus_currency=self.currency,
            days_after_hire_payout=90
        )
        
        # Check that all software jobs have the bonus amount applied
        serialized_software_jobs = self.get_serialized_jobs(self.jobs[:2], [new_rule])
        for job in serialized_software_jobs:
            self.assertEqual(new_rule.base_bonus_amount, job['bonus']['amount'])
            
        # Check that other jobs don't have a bonus amount applied
        serialized_other_jobs = self.get_serialized_jobs(self.jobs[2:], [new_rule])
        for job in serialized_other_jobs:
            self.assertEqual(None, job['bonus']['amount'])
        
        # Add a default bonus amount
        self.employer.default_bonus_amount = 500
        self.employer.default_bonus_currency = self.currency
        self.employer.save()

        # Check that other jobs have default bonus applied
        serialized_other_jobs = self.get_serialized_jobs(self.jobs[2:], [new_rule])
        for job in serialized_other_jobs:
            self.assertEqual(self.employer.default_bonus_amount, job['bonus']['amount'])
            
        # Add bonus modifier that should be applied to the first job (based on days after post)
        modifier = self.create_referral_bonus_rule_modifier(
            new_rule,
            type=EmployerReferralBonusRuleModifier.ModifierType.NOMINAL.value,
            amount=500,
            start_days_after_post=50
        )
        
        # The first job should now have the bonus modifier applied
        job = get_serialized_employer_job(self.jobs[0], rules=[new_rule], is_include_bonus=True)
        self.assertEqual(new_rule.base_bonus_amount + modifier.amount, job['bonus']['amount'])
        
        # The second job should still have the base amount applied
        job = get_serialized_employer_job(self.jobs[1], rules=[new_rule], is_include_bonus=True)
        self.assertEqual(new_rule.base_bonus_amount, job['bonus']['amount'])
        
        # Add another modifier as a percentage. This is applicable to both the first and second job
        # But only the second job should have this modifier applied because the first job still qualifies
        # for the later modifier
        earlier_modifier = self.create_referral_bonus_rule_modifier(
            new_rule,
            type=EmployerReferralBonusRuleModifier.ModifierType.PERCENT.value,
            amount=10,
            start_days_after_post=20
        )

        # The first job should have the original bonus modifier applied
        job = get_serialized_employer_job(self.jobs[0], rules=[new_rule], is_include_bonus=True)
        self.assertEqual(new_rule.base_bonus_amount + modifier.amount, job['bonus']['amount'])

        # The second job should have the new bonus modifier applied
        job = get_serialized_employer_job(self.jobs[1], rules=[new_rule], is_include_bonus=True)
        self.assertEqual(new_rule.base_bonus_amount * (1 + (earlier_modifier.amount / 100)), job['bonus']['amount'])
        