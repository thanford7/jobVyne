from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from jvapp.utils.logger import getLogger

logger = getLogger()


class LoginView(APIView):

    def post(self, request):
        logger.info('Hit login')
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response('Email and password are required', status=HTTPStatus.BAD_REQUEST)

        logger.info('About to authenticate')
        user = authenticate(username=email, password=password)
        if not user:
            return Response('Email or password is incorrect', status=HTTPStatus.UNAUTHORIZED)

        login(request, user)
        return Response(status=HTTPStatus.OK, data={'user_id': user.id})


class LoginSetCookieView(APIView):

    @method_decorator(csrf_exempt)
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        """
        `login_view` requires that a csrf cookie be set.
        `getCsrfToken` in `auth.js` uses this cookie to
        make a request to `login_view`
        """
        return Response('CSRF cookie set', status=HTTPStatus.OK)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=HTTPStatus.OK)
