from rest_framework import status
from rest_framework.response import Response


def handler404(request, exception):
    return Response(status=status.HTTP_404_NOT_FOUND)


def handler500(request):
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
