from jvapp.models.employer import *
from jvapp.utils.datetime import get_date_time_format_or_none


def get_serialized_employer(employer: Employer):
    return {
        'id': employer.id,
        'name': employer.employerName,
        'logo': employer.logo.url if employer.logo else None,
        'description': employer.description,
        'size': employer.employerSize
    }


def get_serialized_employer_job(employer_job: EmployerJob):
    return {
        'id': employer_job.id,
        'employer_id': employer_job.employer_id,
        'job_title': employer_job.jobTitle,
        'job_description': employer_job.jobDescription,
        'job_department': employer_job.jobDepartment,
        'open_date': get_date_time_format_or_none(employer_job.openDate),
        'close_date': get_date_time_format_or_none(employer_job.closeDate),
        'salary_floor': employer_job.salaryFloor,
        'salary_ceiling': employer_job.salaryCeiling,
        'referral_bonus': employer_job.referralBonus,
        'is_full_time': employer_job.isFullTime,
        'is_remote': employer_job.isRemote,
        'location': employer_job.location,
        'city': employer_job.city,
        'state': employer_job.state.stateName,
        'country': employer_job.country.countryName
    }
