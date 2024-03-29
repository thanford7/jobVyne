from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.apis.taxonomy import TaxonomyJobProfessionView


class SearchEntityView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        search_text = request.query_params.get('search_text')
        
        professions = TaxonomyJobProfessionView.get_job_profession_taxonomy(
            search_text=search_text, is_include_subs=True, is_include_job_count=True
        )
        
        # Groups

        # Companies
        return Response(status=status.HTTP_200_OK, data={
            'professions': professions
        })
    