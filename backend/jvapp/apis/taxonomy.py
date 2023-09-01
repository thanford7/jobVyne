from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_success_response, get_warning_response
from jvapp.models.employer import JobTaxonomy, Taxonomy


class TaxonomyJobProfessionView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=self.get_job_profession_taxonomy(is_include_subs=True))
    
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
    def get_job_profession_taxonomy(tax_id=None, tax_key=None, search_text=None, is_include_subs=True,
                                    is_include_job_count=False):
        # Only get parent taxonomies
        tax_filter = Q(tax_type=Taxonomy.TAX_TYPE_PROFESSION)
        if tax_id:
            tax_filter &= Q(id=tax_id)
        elif tax_key:
            tax_filter &= Q(key=tax_key)
        elif search_text:
            tax_filter &= Q(name__iregex=f'^.*{search_text}.*$') | Q(
                sub_taxonomies__name__iregex=f'^.*{search_text}.*$')
        else:
            tax_filter &= Q(parent_taxonomy__isnull=True)
        
        professions = Taxonomy.objects.filter(tax_filter)
        if is_include_subs:
            sub_taxonomy_filter = Q()
            if search_text:
                sub_taxonomy_filter = Q(name__iregex=f'^.*{search_text}.*$')
            sub_profession_prefetch = Prefetch(
                'sub_taxonomies',
                queryset=Taxonomy.objects.filter(sub_taxonomy_filter),
                to_attr='filtered_sub_taxonomies'
            )
            professions = professions.prefetch_related(sub_profession_prefetch)
        
        taxonomy_map = {t: (t.filtered_sub_taxonomies if is_include_subs else []) for t in professions}
        taxonomy_ids = []
        for tax, sub_taxes in taxonomy_map.items():
            taxonomy_ids.append(tax.id)
            for sub_tax in sub_taxes:
                taxonomy_ids.append(sub_tax.id)
        
        # Running two queries for the taxonomies and taxonomy jobs is more efficient
        # than using Django's prefetch with a filter/annotate/count for jobs
        taxonomy_job_count_map = {}
        if is_include_job_count:
            current_job_filter = Q(job__close_date__isnull=True) | Q(job__close_date__gt=timezone.now().date())
            taxonomy_job_count_map = {
                t['taxonomy_id']: t['job_count'] for t in (
                    JobTaxonomy.objects
                    .filter(taxonomy_id__in=taxonomy_ids)
                    .filter(current_job_filter)
                    .values('taxonomy_id')
                    .annotate(job_count=Count('taxonomy_id'))
                )
            }
        
        serialized_professions = []
        for tax, sub_taxes in taxonomy_map.items():
            serialized_tax = TaxonomyJobProfessionView.serialize_profession(tax)
            
            if is_include_job_count:
                serialized_tax['job_count'] = taxonomy_job_count_map.get(tax.id) or 0
            
            if is_include_subs:
                serialized_tax['sub_professions'] = []
                for sub_tax in sub_taxes:
                    serialized_sub_tax = TaxonomyJobProfessionView.serialize_profession(sub_tax)
                    serialized_sub_tax['has_parent'] = True
                    if is_include_job_count:
                        job_count = taxonomy_job_count_map.get(sub_tax.id) or 0
                        serialized_sub_tax['job_count'] = job_count
                        serialized_tax['job_count'] += job_count
                    serialized_tax['sub_professions'].append(serialized_sub_tax)
                serialized_professions.append(serialized_tax)
        
        serialized_professions.sort(key=lambda p: p['name'])
        
        if any((tax_id, tax_key)):
            if not serialized_professions:
                raise Taxonomy.DoesNotExist
            return serialized_professions[0]
        
        return serialized_professions
    
    @staticmethod
    def serialize_profession(profession):
        return {
            'id': profession.id,
            'url': profession.jobs_url,
            'name': profession.name,
            'key': profession.key,
            'description': profession.description
        }
