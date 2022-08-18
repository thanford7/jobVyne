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
        if owner_id := self.query_params.get('owner_id'):
            q_filter = Q(owner_id=owner_id)
        elif employer_id := self.query_params.get('employer_id'):
            q_filter = Q(employer_id=employer_id)
        else:
            return Response('You must provide an owner ID, or employer ID', status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'applications': [],
            'views': []
        }
        app_filter = Q()
        view_filter = Q()
        if start_date:
            app_filter &= Q(created_dt__gte=start_date)
            view_filter &= Q(access_dt__gte=start_date)
        if end_date:
            app_filter &= Q(created_dt__lte=end_date)
            view_filter &= Q(access_dt__lte=end_date)
        for link in SocialLinkFilterView.get_link_filters(self.user, link_filter_filter=q_filter):
            common_data = {
                'link_id': link.id,
                'owner_id': link.owner_id,
                'owner_name': f'{link.owner.first_name} {link.owner.last_name}',
                'platform_name': link.platform.name if link.platform else None
            }
            for app in link.job_application.filter(app_filter):
                data['applications'].append({
                    'id': app.id,
                    'first_name': app.first_name,
                    'last_name': app.last_name,
                    'job_title': app.employer_job.job_title,
                    'apply_dt': get_datetime_format_or_none(app.created_dt),
                    **common_data
                })
            for view in link.page_view.filter(view_filter):
                data['views'].append({
                    'access_dt': get_datetime_format_or_none(view.access_dt),
                    'city': view.city,
                    'region': view.region,
                    'country': view.country,
                    'latitude': view.latitude,
                    'longitude': view.longitude,
                    'is_mobile': bool(view.is_mobile or view.is_tablet),
                    **common_data
                })

        return Response(status=status.HTTP_200_OK, data=data)