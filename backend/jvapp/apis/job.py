import json
import logging
from itertools import groupby

from bs4 import BeautifulSoup
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.employer import EmployerJob, JobDepartment, JobTaxonomy, Taxonomy
from jvapp.models.location import Location
from jvapp.serializers.location import get_serialized_location
from jvapp.utils import ai
from jvapp.utils.ai import PromptError

logger = logging.getLogger(__name__)


class JobDepartmentView(JobVyneAPIView):
    
    def get(self, request):
        JobDepartment.objects.all()
        return Response(status=status.HTTP_200_OK, data=[
            {'id': jd.id, 'name': jd.name} for jd in JobDepartment.objects.all()
        ])
    
    
class LocationView(JobVyneAPIView):
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=self.get_serialized_locations(self.get_locations()))
    
    @staticmethod
    def get_locations():
        return Location.objects.select_related('city', 'state', 'country').all()
    
    @staticmethod
    def get_serialized_locations(location_objects):
        cities, states, countries, locations = {}, {}, {}, {}
        for location in location_objects:
            if not locations.get(location.id):
                locations[location.id] = get_serialized_location(location)
            if location.city and not cities.get(location.city_id):
                cities[location.city_id] = {'name': location.city.name, 'id': location.city.id}
            if location.state and not states.get(location.state_id):
                states[location.state_id] = {'name': location.state.name, 'id': location.state.id}
            if location.country and not countries.get(location.country_id):
                countries[location.country_id] = {'name': location.country.name, 'id': location.country.id}

        return {
            'locations': sorted(list(locations.values()), key=lambda x: (x['is_remote'] or 0, x['city'] or '')),
            'cities': sorted(list(cities.values()), key=lambda x: x['name']),
            'states': sorted(list(states.values()), key=lambda x: x['name']),
            'countries': sorted(list(countries.values()), key=lambda x: x['name'])
        }


class JobClassificationView(JobVyneAPIView):
    def get(self, request):
        taxonomies = Taxonomy.objects.all().order_by('tax_type')
        taxonomies_by_type = groupby(taxonomies, lambda t: t.tax_type)
        jobs = EmployerJob.objects.filter()[:1]
        return Response(status=status.HTTP_200_OK, data={
            'to-classify': {
                j.id: {
                    'title': j.job_title,
                    'description': j.job_description,
                }
                for j in jobs
            },
            'taxonomies': {
                tax_type.name: [t.name for t in taxonomies]
                for tax_type, taxonomies in taxonomies_by_type
            },
        })
    
    def post(self, request):
        limit = self.data.get('limit')
        self.classify_jobs(limit)
        return Response(status=status.HTTP_200_OK)
    
    @staticmethod
    def classify_jobs(limit, is_test=True):
        # Find jobs that have not had their properties set
        jobs = EmployerJob.objects.filter(
            responsibilities__isnull=True,
            qualifications__isnull=True,
            technical_qualifications__isnull=True,
            qualifications_prompt__isnull=True,
        ).filter(Q(close_date__isnull=True) | Q(close_date__gt=timezone.now().date()))

        if limit:
            jobs = jobs[:limit]

        DESCRIPTION_CHAR_LIMIT = 6000  # Prevent exceeding token limit in OpenAI
        RESPONSIBILITY_LIMIT = 5
        QUALIFICATION_LIMIT = 10
        TECH_QUALIFICATION_LIMIT = 10

        for job in jobs:
            prompt = (
                'Use "---" as a delimiter\n'
                f'Create a variable called "JOB_DESCRIPTION" and set it equal to ---\'{job.job_description[:DESCRIPTION_CHAR_LIMIT]}\'---\n'
                f'Analyze the value of JOB_DESCRIPTION and summarize up to {RESPONSIBILITY_LIMIT} job responsibilities, up to {QUALIFICATION_LIMIT} required job qualifications, and up to {TECH_QUALIFICATION_LIMIT} technical qualifications. Examples of technical qualifications include software coding languages, industry certifications, and software tools. Do not list technical qualifications in the job qualifications.\n'
                'Job responsibilities will likely be listed close to the word "responsibilities" in a bulleted list or comma separated list.\n'
                'Job qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
                'Job qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
                'Technical qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
                'The output of your answer should be JSON in the format:\n'
                f'{{"JOB_RESPONSIBILITIES": [], "JOB_QUALIFICATIONS": [], "TECHNICAL_QUALIFICATIONS": []}}\n'
            )
            try:
                resp, tracker = ai.ask(prompt)
                job.qualifications_prompt = tracker
                job.qualifications = resp.get('JOB_QUALIFICATIONS')
                job.technical_qualifications = resp.get('TECHNICAL_QUALIFICATIONS')
                job.responsibilities = resp.get('JOB_RESPONSIBILITIES')
            except PromptError:
                pass

            if not is_test:
                job.save()

