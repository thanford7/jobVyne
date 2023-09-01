from django.db.models import Count, Prefetch, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_success_response, get_warning_response
from jvapp.models.employer import Taxonomy


class TaxonomyJobProfessionView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=[
            self.serialize_profession(p) for p in self.get_job_profession_taxonomy()
        ])
    
    def put(self, request):
        tax = Taxonomy.objects.get(self.data['tax_id'])
        tax.name = self.data['name']
        tax.save()
        return get_success_response('Taxonomy updated')
        
    def post(self, request):
        try:
            Taxonomy.objects.get(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name=self.data['name'])
            return get_warning_response('Taxonomy already exists')
        except Taxonomy.DoesNotExist:
            Taxonomy(tax_type=Taxonomy.TAX_TYPE_PROFESSION, name=self.data['name']).save()
            return get_success_response('Taxonomy created')
        
    @staticmethod
    def get_job_profession_taxonomy(tax_id=None, tax_key=None, search_text=None):
        # Only get parent taxonomies
        tax_filter = Q(tax_type=Taxonomy.TAX_TYPE_PROFESSION)
        if tax_id:
            tax_filter &= Q(id=tax_id)
        elif tax_key:
            tax_filter &= Q(key=tax_key)
        elif search_text:
            tax_filter &= Q(name__iregex=f'^.*{search_text}.*$') | Q(sub_taxonomies__name__iregex=f'^.*{search_text}.*$')
        else:
            tax_filter &= Q(parent_taxonomy__isnull=True)
        
        sub_taxonomy_filter = Q()
        if search_text:
            sub_taxonomy_filter = Q(name__iregex=f'^.*{search_text}.*$')
        sub_profession_prefetch = Prefetch(
            'sub_taxonomies',
            queryset=Taxonomy.objects.filter(sub_taxonomy_filter).annotate(job_count=Count('job')),
            to_attr='filtered_sub_taxonomies'
        )
            
        taxes = (
            Taxonomy.objects
            .prefetch_related(sub_profession_prefetch)
            .filter(tax_filter)
            .annotate(job_count=Count('job'))
            .order_by('name')
        )
        if any((tax_id, tax_key)):
            if not taxes:
                raise Taxonomy.DoesNotExist
            return taxes[0]
        
        return taxes
    
    @staticmethod
    def serialize_profession(profession):
        total_job_count = 0
        sub_professions = []
        for sp in profession.filtered_sub_taxonomies:
            sub_professions.append({
                'id': sp.id,
                'url': sp.jobs_url,
                'name': sp.name,
                'key': sp.key,
                'description': sp.description,
                'job_count': sp.job_count
            })
            total_job_count += sp.job_count
        
        return {
            'id': profession.id,
            'url': profession.jobs_url,
            'name': profession.name,
            'key': profession.key,
            'description': profession.description,
            'sub_professions': sub_professions,
            'job_count': total_job_count
        }
    