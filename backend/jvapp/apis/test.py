from rest_framework.views import APIView

from jvapp.permissions.general import IsAdmin


class TestErrorView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        raise ValueError('This is a test error message')
