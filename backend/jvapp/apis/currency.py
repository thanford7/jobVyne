from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.models.currency import Currency


class CurrencyView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=[
            {'id': c.id, 'name': c.name, 'symbol': c.symbol} for c in Currency.objects.all()
        ])
