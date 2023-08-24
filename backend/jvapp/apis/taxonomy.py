from django.db.models import Q
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
    def get_job_profession_taxonomy(tax_id=None, tax_key=None):
        # Only get parent taxonomies
        tax_filter = Q(tax_type=Taxonomy.TAX_TYPE_PROFESSION)
        if tax_id:
            tax_filter &= Q(id=tax_id)
        elif tax_key:
            tax_filter &= Q(key=tax_key)
        else:
            tax_filter &= Q(parent_taxonomy__isnull=True)
            
        taxes = Taxonomy.objects.prefetch_related('sub_taxonomies').filter(tax_filter).order_by('name')
        if any((tax_id, tax_key)):
            if not taxes:
                raise Taxonomy.DoesNotExist
            return taxes[0]
        
        return taxes
    
    @staticmethod
    def serialize_profession(profession):
        return {
            'id': profession.id,
            'name': profession.name,
            'key': profession.key,
            'description': profession.description,
            'sub_professions': [{
                'id': sp.id,
                'name': sp.name,
                'key': sp.key,
                'description': sp.description,
            } for sp in profession.sub_taxonomies.all()]
        }
    