from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, get_success_response, get_warning_response
from jvapp.models.employer import Taxonomy


class TaxonomyJobTitleView(JobVyneAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=[
            {
                'id': t.id,
                'name': t.name
            } for t in Taxonomy.objects.filter(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE)
        ])
    
    def put(self, request):
        tax = Taxonomy.objects.get(self.data['tax_id'])
        tax.name = self.data['name']
        tax.save()
        return get_success_response('Taxonomy updated')
        
    def post(self, request):
        try:
            Taxonomy.objects.get(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name=self.data['name'])
            return get_warning_response('Taxonomy already exists')
        except Taxonomy.DoesNotExist:
            Taxonomy(tax_type=Taxonomy.TAX_TYPE_JOB_TITLE, name=self.data['name']).save()
            return get_success_response('Taxonomy created')
    