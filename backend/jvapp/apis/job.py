import json
import logging
from itertools import groupby

from bs4 import BeautifulSoup
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.employer import EmployerJob, JobDepartment, JobTaxonomy, Taxonomy
from jvapp.models.location import Location
from jvapp.serializers.location import get_serialized_location
from jvapp.utils import ai

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
        # Find jobs that have not yet been 'bucketed'
        jobs = EmployerJob.objects\
            .annotate(job_taxonomy_count=Count('jobtaxonomy'))\
            .filter(job_taxonomy_count__lt=len(Taxonomy.ALL_TAX_TYPES))
        
        if limit:
            jobs = jobs[:limit]
    
        taxonomies = Taxonomy.objects.all().order_by('tax_type')
        taxonomies_by_type = {
            tax_type: ', '.join(list(t.name for t in tax_list)) for tax_type, tax_list in
            groupby(taxonomies, lambda t: t.tax_type)
        }
        taxonomy_map = {
            (t.tax_type, t.name): t for t in Taxonomy.objects.all()
        }
        job_taxonomies = []
        for job in jobs:
            prompt = (
                'You are helping to classify job descriptions into buckets of standardized categories.'
                'You must pick a standardized category for:\n'
                f'<{Taxonomy.TAX_TYPE_JOB_TITLE}>\n'
                f'<{Taxonomy.TAX_TYPE_JOB_LEVEL}>\n'
                f'There can be only one category for <{Taxonomy.TAX_TYPE_JOB_TITLE}> and one category <{Taxonomy.TAX_TYPE_JOB_LEVEL}>.\n'
                f'The available <{Taxonomy.TAX_TYPE_JOB_TITLE}> category options are:\n'
                f'[{taxonomies_by_type[Taxonomy.TAX_TYPE_JOB_TITLE]}]\n'
                f'The available <{Taxonomy.TAX_TYPE_JOB_LEVEL}> options are:\n'
                f'[{taxonomies_by_type[Taxonomy.TAX_TYPE_JOB_LEVEL]}]\n'
                f'The output of your response should be JSON in the format:\n'
                f'{{"{Taxonomy.TAX_TYPE_JOB_LEVEL}": <{Taxonomy.TAX_TYPE_JOB_LEVEL}>, "{Taxonomy.TAX_TYPE_JOB_TITLE}": <{Taxonomy.TAX_TYPE_JOB_TITLE}>}}\n'
                f'Choose the <{Taxonomy.TAX_TYPE_JOB_LEVEL}> and <{Taxonomy.TAX_TYPE_JOB_TITLE}> for the following job description:\n'
                f'{job.job_title}\n{BeautifulSoup(job.job_description).text}\n'
            )
            resp = ai.ask(prompt)
            categorizations = json.loads(resp['choices'][0]['text'])
            print(categorizations)
            
            # TODO: Add this as metadata somewhere
            completion_model = resp['model']
            total_tokens_used = resp['usage']['total_tokens']
            
            for tax_type in [Taxonomy.TAX_TYPE_JOB_TITLE, Taxonomy.TAX_TYPE_JOB_LEVEL]:
                val = categorizations[tax_type]
                tax = taxonomy_map.get((tax_type, val))
                if not tax:
                    logger.error(f'Could not find taxonomy {val} for taxonomy type {tax_type}. Job ID = {job.id}')
                    continue
                job_taxonomies.append(JobTaxonomy(job=job, taxonomy=tax))
        
        if not is_test:
            JobTaxonomy.objects.bulk_create(job_taxonomies)
