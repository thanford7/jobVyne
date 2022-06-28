import requests
from django.conf import settings

OAUTH_CFGS = {
    'google': {
        'token_url': 'https://oauth2.googleapis.com/token',
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'auth_params': {
            'state': settings.AUTH_STATE,
            # nonce: 'forewijf43oirjoifj',
            'response_type': 'code',
            'scope': 'openid email',
            'redirect_uri': f'{settings.FRONTEND_URL}auth/google/callback',
            'login_hint': ''
        }
    },
    'facebook': {
        'token_url': 'https://graph.facebook.com/v14.0/oauth/access_token',
        'auth_url': 'https://www.facebook.com/v14.0/dialog/oauth',
        'auth_params': {
            'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
            'state': settings.AUTH_STATE,
            'scope': 'email',
            'redirect_uri': f'{settings.FRONTEND_URL}auth/facebook/callback',
        }
    },
}

SOCIAL_AUTH_PREFIX = 'SOCIAL_AUTH_'


def get_payload(backend, code):

    client_id = getattr(settings, f'{SOCIAL_AUTH_PREFIX}{backend.upper()}_KEY')
    client_secret = getattr(settings, f'{SOCIAL_AUTH_PREFIX}{backend.upper()}_SECRET')
    if not all([client_id, client_secret]):
        raise ValueError('OAuth client key and secret are required')

    payload = None
    redirect_uri = OAUTH_CFGS[backend]['auth_params']['redirect_uri']
    if backend == 'google':
        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': "authorization_code",
        }
    elif backend == 'facebook':
        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        
    if not payload:
        raise ValueError(f'{backend} is not a valid option')

    return payload


def get_access_token_from_code(backend, code):
    """Get access token for any OAuth backend from code"""

    url = OAUTH_CFGS[backend]['token_url']
    payload = get_payload(backend, code)

    # different providers have different responses to their oauth endpoint
    if backend == 'google':
        r = requests.post(url, data=payload)

        token = r.json()['access_token']

        return token

    elif backend == 'facebook':
        r = requests.get(url, params=payload)
        token = r.json()['access_token']
        return token
