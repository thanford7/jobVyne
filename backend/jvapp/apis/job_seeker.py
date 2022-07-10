from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jvapp.apis._apiBase import JobVyneAPIView, SUCCESS_MESSAGE_KEY
from jvapp.models import JobVyneUser


class ApplicationView(JobVyneAPIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Save application to Django model
        
        # Save or update application template to Django model
        
        # Update user if they don't have the candidate bit set
        if not self.user.is_candidate:
            self.user.user_type_bits |= JobVyneUser.USER_TYPE_CANDIDATE
            self.user.save()
        
        # Push application to ATS integration
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                # TODO: Add employer and job title to success message
                SUCCESS_MESSAGE_KEY: 'Your application was submitted'
            }
        )
