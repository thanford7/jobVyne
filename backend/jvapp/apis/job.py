import asyncio
import logging
from itertools import groupby

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.models.employer import EmployerJob, JobDepartment, Taxonomy
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
    DESCRIPTION_CHAR_LIMIT = 5100  # Prevent exceeding token limit in OpenAI
    RESPONSIBILITY_LIMIT = 5
    QUALIFICATION_LIMIT = 10
    TECH_QUALIFICATION_LIMIT = 10
    CONCURRENT_REQUESTS = 10
    
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

        system_prompt = (
            'You are helping categorize job descriptions. The use will provide an individual job description for you to categorize.\n'
            f'Analyze the job description and categorize up to {JobClassificationView.RESPONSIBILITY_LIMIT} job responsibilities, up to {JobClassificationView.QUALIFICATION_LIMIT} required job qualifications, and up to {JobClassificationView.TECH_QUALIFICATION_LIMIT} technical qualifications. Examples of technical qualifications include software coding languages, industry certifications, and software tools. Do not list technical qualifications in the job qualifications.\n'
            'Job responsibilities will likely be listed close to the word "responsibilities" in a bulleted list or comma separated list.\n'
            'Job qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
            'Job qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
            'Technical qualifications will likely be listed close to the word "qualifications" or "skills" in a bulleted list or comma separated list.\n'
            'Your response should make sure to use proper capitalization and punctuation, especially for proper nouns. Your response should be RFC8259 compliant JSON in the format:\n'
            f'{{"JOB_RESPONSIBILITIES": [], "JOB_QUALIFICATIONS": [], "TECHNICAL_QUALIFICATIONS": []}}\n'
        )
        
        job_idx = 0
        while job_idx < len(jobs):
            jobs_to_process = jobs[job_idx:job_idx+JobClassificationView.CONCURRENT_REQUESTS]
            asyncio.run(
                JobClassificationView.process_jobs(jobs_to_process, system_prompt, is_test)
            )

            if not is_test:
                EmployerJob.objects.bulk_update(
                    jobs_to_process,
                    ['qualifications_prompt', 'qualifications', 'technical_qualifications', 'responsibilities']
                )
                
            job_idx += JobClassificationView.CONCURRENT_REQUESTS
                
    @staticmethod
    async def summarize_job(system_prompt, is_test, queue):
        while True:
            job = await queue.get()
            logger.info(f'Running job classification for job ID = {job.id}')
            trunc_job_description = job.job_description[:JobClassificationView.DESCRIPTION_CHAR_LIMIT]
            try:
                if is_test:
                    logger.info('----- SYSTEM PROMPT')
                    logger.info(system_prompt)
                    logger.info('----- USER PROMPT')
                    logger.info(trunc_job_description)
                resp, tracker = await ai.ask([
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': trunc_job_description}
                ], is_test=is_test)
                job.qualifications_prompt = tracker
                job.qualifications = resp.get('JOB_QUALIFICATIONS')
                job.technical_qualifications = resp.get('TECHNICAL_QUALIFICATIONS')
                job.responsibilities = resp.get('JOB_RESPONSIBILITIES')
            except PromptError:
                pass
        
            queue.task_done()
        
    @staticmethod
    async def process_jobs(jobs, system_prompt, is_test):
        queue = asyncio.Queue()
        workers = [
            asyncio.create_task(JobClassificationView.summarize_job(system_prompt, is_test, queue))
            for _ in range(JobClassificationView.CONCURRENT_REQUESTS)
        ]
        
        for job in jobs:
            await queue.put(job)

        # Wait until the queue is fully processed
        if not queue.empty():
            logger.info(f'Waiting for job queue to finish - Currently {queue.qsize()}')
            done, _ = await asyncio.wait([queue.join(), *workers], return_when=asyncio.FIRST_COMPLETED)
            consumers_raised = set(done) & set(workers)
            if consumers_raised:
                logger.info(f'Found {len(consumers_raised)} consumers that raised exceptions')
                await consumers_raised.pop()  # propagate the exception

        for worker in workers:
            worker.cancel()
        
        # Wait until all workers are cancelled
        await asyncio.gather(*workers, return_exceptions=True)
        logger.info(f'Completed summarizing {len(jobs)} jobs')
