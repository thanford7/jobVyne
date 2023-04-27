from datetime import timedelta
from random import choice, choices, randint, random

import names
import pytz
from django.db import IntegrityError
from django.utils import timezone
from faker import Faker
from numpy.random import poisson

from jvapp.apis.job_seeker import ApplicationView
from jvapp.apis.social import SocialLinkJobsView
from jvapp.apis.tracking import set_user_agent_data
from jvapp.models import City, Country, Employer, EmployerJob, EmployerReferralBonusRule, \
    EmployerReferralBonusRuleModifier, JobApplication, JobDepartment, \
    JobVyneUser, Location, \
    PageView, SocialLinkFilter, \
    SocialPlatform, State


fake = Faker()


def generate_user(employer, user_type_bits=JobVyneUser.USER_TYPE_EMPLOYEE, email_domain='gmail.com'):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = f'{first_name}_{last_name}@{email_domain}'
    try:
        user = JobVyneUser.objects.create_user(
            email, first_name=first_name, last_name=last_name, user_type_bits=user_type_bits, employer=employer
        )
    except IntegrityError:
        user = JobVyneUser.objects.get(email=email)
    return user

 
def generate_employer(employer_name, email_domains='gmail.com', default_bonus_amount=1000, default_bonus_currency='USD'):
    try:
        employer = Employer(
            employer_name=employer_name,
            email_domains=email_domains,
            default_bonus_amount=default_bonus_amount,
            default_bonus_currency_id=default_bonus_currency
        )
        employer.save()
    except IntegrityError:
        employer = Employer.objects.get(employer_name=employer_name)
    return employer
    
    
def generate_job_department(name):
    try:
        dept = JobDepartment(name=name)
        dept.save()
    except IntegrityError:
        dept = JobDepartment.objects.get(name=name)
    return dept


def generate_city(name):
    try:
        city = City(name=name)
        city.save()
    except IntegrityError:
        city = City.objects.get(name=name)
    return city


def generate_state(name):
    try:
        state = State(name=name)
        state.save()
    except IntegrityError:
        state = State.objects.get(name=name)
    return state


def generate_country(name):
    try:
        country = Country(name=name)
        country.save()
    except IntegrityError:
        country = Country.objects.get(name=name)
    return country


def generate_location(text, city, state, country):
    try:
        location = Location(
            text=text,
            city=city,
            state=state,
            country=country
        )
        location.save()
    except IntegrityError:
        location = Location.objects.get(text=text)
    return location


def generate_employer_job(
        employer, job_title, job_department, open_date, locations,
        salary_floor=None, salary_ceiling=None, referral_bonus=None
):
    job = EmployerJob(
        employer=employer,
        job_title=job_title,
        job_department=job_department,
        open_date=open_date,
        salary_floor=salary_floor,
        salary_ceiling=salary_ceiling,
        referral_bonus=referral_bonus
    )
    job.save()
    for location in locations:
        job.locations.add(location)


def generate_social_link(owner, employer, departments=None, cities=None, states=None, countries=None):
    link = SocialLinkFilter(
        owner=owner,
        employer=employer
    )
    link.save()
    for department in departments or []:
        link.departments.add(department)
    for city in cities or []:
        link.cities.add(city)
    for state in states or []:
        link.states.add(state)
    for country in countries or []:
        link.countries.add(country)
        
        
def generate_employer_referral_bonus_rule(
        employer, order_idx, base_bonus_amount, days_after_hire_payout=90,
        include_departments=None, exclude_departments=None,
        include_cities=None, exclude_cities=None,
        include_states=None, exclude_states=None,
        include_countries=None, exclude_countries=None,
):
    try:
        return EmployerReferralBonusRule.objects.get(employer=employer, order_idx=order_idx)
    except EmployerReferralBonusRule.DoesNotExist:
        rule = EmployerReferralBonusRule(
            employer=employer,
            order_idx=order_idx,
            base_bonus_amount=base_bonus_amount,
            days_after_hire_payout=days_after_hire_payout
        )
        rule.save()
    
        for dept in include_departments or []:
            rule.include_departments.add(dept)
        for dept in exclude_departments or []:
            rule.exclude_departments.add(dept)
    
        for city in include_cities or []:
            rule.include_cities.add(city)
        for city in exclude_cities or []:
            rule.exclude_cities.add(city)
    
        for state in include_states or []:
            rule.include_states.add(state)
        for state in exclude_states or []:
            rule.exclude_states.add(state)
    
        for country in include_countries or []:
            rule.include_countries.add(country)
        for country in exclude_countries or []:
            rule.exclude_countries.add(country)
    
        return rule


def generate_bonus_rule_modifier(
        bonus_rule, amount, start_days_after_post, type=EmployerReferralBonusRuleModifier.ModifierType.NOMINAL.value
):
    kwargs = {
        'referral_bonus_rule': bonus_rule,
        'amount': amount,
        'type': type,
        'start_days_after_post': start_days_after_post
    }
    try:
        return EmployerReferralBonusRuleModifier.objects.get(**kwargs)
    except EmployerReferralBonusRuleModifier.DoesNotExist:
        modifier = EmployerReferralBonusRuleModifier(**kwargs)
        modifier.save()
        return modifier
    
    
def generate_job_application(social_link_filter, job, platform):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = fake.ascii_free_email()
    current_dt = timezone.now()
    application_dt = fake.date_time_between(current_dt - timedelta(days=7), current_dt).replace(tzinfo=pytz.UTC)
    try:
        application = JobApplication(
            first_name=first_name,
            last_name=last_name,
            email=email,
            linkedin_url=f'https://www.linkedin.com/in/{first_name}-{last_name}/',
            social_link_filter=social_link_filter,
            platform=platform,
            employer_job=job,
            created_dt=application_dt,
            modified_dt=application_dt
        )
        ApplicationView.add_application_referral_bonus(application)
        application.save()
    except IntegrityError:
        application = JobApplication.objects.get(email=email, employer_job=job)
    return application


def generate_page_view(social_link, platform, access_dt=None):
    ip_address = fake.ipv4_public()
    current_dt = timezone.now()
    lat, long, city, country, state = fake.local_latlng()
    state = state.split('/')[-1].replace('_', ' ')
    page_view = PageView(
        relative_url=f'social-link-filter/{social_link.id}/',
        social_link_filter=social_link,
        platform=platform,
        ip_address=ip_address,
        access_dt=access_dt or fake.date_time_between(current_dt - timedelta(days=7), current_dt).replace(tzinfo=pytz.UTC),
        city=city,
        country=country,
        region=state,
        latitude=lat,
        longitude=long
    )
    set_user_agent_data(page_view, fake.user_agent())
    page_view.save()
    return page_view


def create_ancillary_data():
    for employer_name in ('Google', 'Vandelay Industries', 'JobVyne'):
        employer = generate_employer(employer_name)
        users = [generate_user(employer) for _ in range(40)]
        
        departments = [
            generate_job_department(dept)
            for dept in ['Software Engineering', 'Product Management', 'Sales', 'Marketing', 'Strategy']
        ]
        
        locations = []
        cities = set()
        states = set()
        countries = set()
        for location_data in (
            ('Austin', 'TX', 'USA'),
            ('Dallas', 'TX', 'USA'),
            ('Los Angeles', 'CA', 'USA'),
            ('San Francisco', 'CA', 'USA'),
            ('Denver', 'CO', 'USA'),
            ('Boston', 'MA', 'USA')
        ):
            city = generate_city(location_data[0])
            state = generate_state(location_data[1])
            country = generate_country(location_data[2])
            cities.add(city)
            states.add(state)
            countries.add(country)
            locations.append(generate_location(', '.join(location_data), city, state, country))
    
        cities = list(cities)
        states = list(states)
        countries = list(countries)
    
        current_dt = timezone.now()
        jobs = []
        for job_title, dept in (
            ('Software Engineer - L1', departments[0]),
            ('Software Engineer - L3', departments[0]),
            ('Software Engineer Manager', departments[0]),
            ('Product Manager', departments[1]),
            ('Senior Product Manager', departments[1]),
            ('Sales Development Representative', departments[2]),
            ('Sales Director', departments[2]),
            ('Digital Marketing Analyst', departments[3]),
            ('Strategy Consultant', departments[4]),
        ):
            for _ in range(randint(1, 4)):
                locations = list({location for location in choices(locations, k=randint(1, 3))})
                open_date = fake.date_between(current_dt - timedelta(days=60), current_dt)
                salary_floor = randint(60000, 120000)
                salary_ceiling = salary_floor + randint(10000, 40000)
                jobs.append(generate_employer_job(
                    employer, job_title, dept, open_date, locations,
                    salary_floor=salary_floor, salary_ceiling=salary_ceiling
                ))
        
        platforms = list(SocialPlatform.objects.all())
        for user in users:
            for _ in range(randint(2, 5)):
                include_department = randint(0, 1)
                include_cities = randint(0, 1)
                include_states = randint(0, 1)
                include_country = randint(0, 1)
                social_department = [choice(departments)] if include_department else None
                social_cities = list({city for city in choices(cities)}) if include_cities else None
                social_states = list({state for state in choices(states)}) if include_states else None
                social_country = [choice(countries)] if include_country else None
                generate_social_link(
                    user, employer,
                    departments=social_department, cities=social_cities,
                    states=social_states, countries=social_country
                )
        
        bonus_rules = []
        for idx, data in enumerate((
            (1500, {
                'include_departments': departments[0:2]
            }),
            (2500, {
                'include_states': [states[1], states[3]]
            }),
            (3000, {
                'exclude_cities': cities[2:4]
            }),
        )):
            bonus = data[0]
            kwargs = data[1]
            bonus_rules.append(generate_employer_referral_bonus_rule(employer, idx, bonus, **kwargs))
            
        generate_bonus_rule_modifier(bonus_rules[1], 1000, 30)
        generate_bonus_rule_modifier(bonus_rules[1], 50, 50, type=EmployerReferralBonusRuleModifier.ModifierType.PERCENT.value)
    
    
def create_recurring_data():
    employers = Employer.objects.filter(employer_name__in=('Hospital IQ', 'Google', 'Vandelay Industries'))
    platforms = list(SocialPlatform.objects.all())
    for employer in employers:
        users = JobVyneUser.objects.filter(employer=employer)
        social_link_filters = SocialLinkFilter.objects.filter(owner_id__in=[u.id for u in users])
        for social_link in social_link_filters:
            jobs = SocialLinkJobsView.get_jobs_from_filter(link_filter=social_link)
            if not jobs:
                continue
            application_count = int(poisson(lam=3.0))
            view_count = int(application_count * randint(10, 100) * random())
            platform = choice(platforms)
            for _ in range(application_count):
                generate_job_application(social_link, choice(jobs), platform)
            for _ in range(view_count):
                generate_page_view(social_link, platform)
            
    print('Data creation complete')
