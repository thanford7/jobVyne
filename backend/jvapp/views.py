from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def handler404(request, exception):
    return Response(status=status.HTTP_404_NOT_FOUND)


def handler500(request):
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
