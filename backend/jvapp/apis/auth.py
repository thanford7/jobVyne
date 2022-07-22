from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
from requests import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.utils import psa

from jvapp.models import JobVyneUser
from jvapp.serializers.user import get_serialized_user
from jvapp.utils.logger import getLogger
from jvapp.utils.oauth import get_access_token_from_code, OAUTH_CFGS

logger = getLogger()

# https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
ALLOWABLE_CAPTCHA_RISK_SCORE = 0.5


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response('Email and password are required', status=HTTPStatus.BAD_REQUEST)
        
        user = authenticate(username=email, password=password)
        if not user:
            return Response('Email or password is incorrect', status=HTTPStatus.UNAUTHORIZED)
        
        login(request, user)
        return Response(status=HTTPStatus.OK, data={'user_id': user.id})


class LoginSetCookieView(APIView):
    permission_classes = [AllowAny]
    
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


class CheckAuthView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if not all((request.user, request.user.is_authenticated)):
            return Response(status=status.HTTP_200_OK, data=False)
        
        return Response(
            status=status.HTTP_200_OK,
            data=get_serialized_user(request.user)
        )


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def social_auth(request, backend):
    """
        Exchange an OAuth2 access token for one for this site.
        This simply defers the entire OAuth2 process to the front end.
        The front end becomes responsible for handling the entirety of the
        OAuth2 process; we just step in at the end and use the access token
        to populate some user identity.
        The URL at which this view lives must include a backend field, like:
            url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
        Using that example, you could call this endpoint using i.e.
            POST API_ROOT + 'social/facebook/'
            POST API_ROOT + 'social/google-oauth2/'
        Note that those endpoint examples are verbatim according to the
        PSA backends which we configured in settings.py. If you wish to enable
        other social authentication backends, they'll get their own endpoints
        automatically according to PSA.
        ## Request format
        Requests must include the following field
        - `access_token`: The OAuth2 access token provided by the provider
        """
    
    code = request.data.get('code', '').strip()
    if not code:
        return Response('An auth token is required', status=status.HTTP_400_BAD_REQUEST)
    
    state = request.data.get('state', '').strip()
    if state != settings.AUTH_STATE:
        return Response('Request state is not the same as the callback state', status=status.HTTP_401_UNAUTHORIZED)
    
    access_token = get_access_token_from_code(backend, code)
    
    try:
        # this line, plus the psa decorator above, are all that's
        # necessary to get and populate a user object for any properly
        # enabled/configured backend which python-social-auth can handle.
        user = request.backend.do_auth(access_token, user_type_bits=JobVyneUser.USER_TYPE_EMPLOYEE)
    except HTTPError as e:
        # An HTTPError bubbled up from the request to the social
        # auth provider. This happens, at least in Google's case, every time you
        # send a malformed or incorrect access key.
        return Response(f'Invalid token: {e}', status=status.HTTP_400_BAD_REQUEST)
    
    if not user:
        # Unfortunately, PSA swallows any information the backend provider
        # generated as to why specifically the authentication failed;
        # this makes it tough to debug except by examining the server logs.
        return Response('Authentication failed', status=status.HTTP_400_BAD_REQUEST)
    
    if user.is_active:
        login(request, user)
        return Response(status=status.HTTP_200_OK, data={'user_id': user.id})
    else:
        return Response('User is not active', status=status.HTTP_401_UNAUTHORIZED)


class SocialAuthCredentialsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=OAUTH_CFGS)


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
def validate_recaptcha(request):
    data = request.data
    try:
        risk_score = create_assessment(settings.GOOGLE_PROJECT_ID, settings.GOOGLE_CAPTCHA_SITE_KEY, data.get('token'),
                                 data.get('action'))
    except Exception as e:
        logger.info(e)
    if not risk_score:
        raise PermissionError('reCAPTCHA authentication failed')
    
    return Response(status=status.HTTP_200_OK, data={'score': risk_score})


def create_assessment(
        project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str
) -> Assessment:
    """Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """
    
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()
    
    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token
    
    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event
    
    project_name = f"projects/{project_id}"
    
    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name
    
    response = client.create_assessment(request)
    
    # Check if the token is valid.
    if not response.token_properties.valid:
        errorMsg = (
            "The CreateAssessment call failed because the token was "
            + "invalid for for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        logger.error(errorMsg)
        raise PermissionError(errorMsg)
    
    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        errorMsg = (
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        logger.error(errorMsg)
        raise PermissionError(errorMsg)
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            logger.error(reason)
        logger.error(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (id). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        logger.error(f"Assessment name: {assessment_name}")
        if response.risk_analysis.score < ALLOWABLE_CAPTCHA_RISK_SCORE:
            raise PermissionError('Failed reCAPTCHA validation')
    return response.risk_analysis.score
