from collections import defaultdict

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView
from jvapp.apis.social import SocialLinkFilterView
from jvapp.utils.datetime import get_datetime_format_or_none, get_datetime_or_none


class DataLinkPerformanceView(JobVyneAPIView):
    
    def get(self, request):
        start_date = get_datetime_or_none(self.query_params.get('start_date'), format='%m/%d/%Y', asDate=True)
        end_date = get_datetime_or_none(self.query_params.get('end_date'), format='%m/%d/%Y', asDate=True)
        owner_id = self.query_params.get('owner_id')
        employer_id = self.query_params.get('employer_id')
        q_filter = Q()
        if owner_id:
            owner_id = int(owner_id)
            q_filter &= Q(owner_id=owner_id)
        if employer_id:
            employer_id = int(employer_id)
            q_filter &= Q(employer_id=employer_id)
        if not any([owner_id, employer_id]):
            return Response('You must provide an owner ID, or employer ID', status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'applications': [],
            'views': []
        }
        
        is_employer = self.user.is_employer and employer_id and self.user.employer_id == employer_id
        for link in SocialLinkFilterView.get_link_filters(
                self.user, link_filter_filter=q_filter, start_date=start_date, end_date=end_date, is_use_permissions=False
        ):
            is_owner = link.owner_id == self.user.id
            common_data = {
                'link_id': link.id,
                'owner_id': link.owner_id,
                'owner_first_name': link.owner.first_name,
                'owner_last_name': link.owner.last_name,
                'platform_name': link.platform.name if link.platform else 'Unknown'
            }
            for app in link.job_application.all():
                application_data = {
                    'id': app.id,
                    'job_title': app.employer_job.job_title,
                    'apply_dt': get_datetime_format_or_none(app.created_dt),
                }
                if is_employer or is_owner:
                    application_data['first_name'] = app.first_name
                    application_data['last_name'] = app.last_name
                data['applications'].append({
                    **application_data,
                    **common_data
                })
            views = defaultdict(int)
            for view in link.page_view.all():
                views[(
                    get_datetime_format_or_none(view.access_dt),
                    bool(view.is_mobile or view.is_tablet)
                )] += 1
            
            for view_key, view_count in views.items():
                data['views'].append({
                    'access_dt': view_key[0],
                    'is_mobile': view_key[1],
                    'view_count': view_count,
                    **common_data
                })

        return Response(status=status.HTTP_200_OK, data=data)