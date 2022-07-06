from jvapp.models.employer import *
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_employer(employer: Employer):
    return {
        'id': employer.id,
        'name': employer.employerName,
        'logo': employer.logo.url if employer.logo else None,
        'description': employer.description,
        'size': employer.employerSize.size
    }


def get_serialized_employer_job(employer_job: EmployerJob):
    return {
        'id': employer_job.id,
        'employer_id': employer_job.employer_id,
        'job_title': employer_job.jobTitle,
        'job_description': employer_job.jobDescription,
        'job_department': employer_job.jobDepartment.name if employer_job.jobDepartment else None,
        'job_department_id': employer_job.jobDepartment_id,
        'open_date': get_datetime_format_or_none(employer_job.openDate),
        'close_date': get_datetime_format_or_none(employer_job.closeDate),
        'salary_floor': employer_job.salaryFloor,
        'salary_ceiling': employer_job.salaryCeiling,
        'referral_bonus': employer_job.referralBonus,
        'is_full_time': employer_job.isFullTime,
        'is_remote': employer_job.isRemote,
        'location': employer_job.location,
        'city': employer_job.city,
        'state': employer_job.state.stateName,
        'state_id': employer_job.state_id,
        'country': employer_job.country.countryName,
        'country_id': employer_job.country_id
    }
