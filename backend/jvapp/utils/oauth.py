from enum import Enum

import requests
from django.conf import settings
from social_core.utils import parse_qs


class OauthProviders(Enum):
    google = 'google-oauth2'
    facebook = 'facebook'
    linkedin = 'linkedin-oauth2'

OAUTH_CFGS = {
    OauthProviders.google.value: {
        'backend_key': 'GOOGLE',
        'name': 'Google',
        'token_url': 'https://oauth2.googleapis.com/token',
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'auth_params': {
            'client_id': settings.SOCIAL_AUTH_GOOGLE_KEY,
            'state': settings.AUTH_STATE,
            'response_type': 'code',
            'login_scope': 'profile email',
            'scope': 'profile email https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly',
            'access_type': 'offline',
            'include_granted_scopes': 'true',
            'redirect_uri': f'{settings.FRONTEND_URL}auth/google-oauth2/callback',
        }
    },
    OauthProviders.facebook.value: {
        'backend_key': 'FACEBOOK',
        'name': 'Facebook',
        'token_url': 'https://graph.facebook.com/v14.0/oauth/access_token',
        'auth_url': 'https://www.facebook.com/v14.0/dialog/oauth',
        'auth_params': {
            'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
            'state': settings.AUTH_STATE,
            'login_scope': 'email',
            'scope': 'email',
            'redirect_uri': f'{settings.FRONTEND_URL}auth/facebook/callback',
        }
    },
    OauthProviders.linkedin.value: {
        'backend_key': 'LINKEDIN',
        'name': 'LinkedIn',
        'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'auth_params': {
            'client_id': settings.SOCIAL_AUTH_LINKEDIN_KEY,
            'state': settings.AUTH_STATE,
            'response_type': 'code',
            'login_scope': 'r_emailaddress r_liteprofile',
            'scope': 'r_emailaddress r_liteprofile w_member_social',
            'redirect_uri': f'{settings.FRONTEND_URL}auth/linkedin-oauth2/callback',
        }
    },
}

SOCIAL_AUTH_PREFIX = 'SOCIAL_AUTH_'


def get_payload(backend, code):
    if not (backend_cfg := OAUTH_CFGS.get(backend)):
        raise ValueError(f'{backend} is not a valid option')
    
    backend_key = backend_cfg['backend_key']
    client_id = getattr(settings, f'{SOCIAL_AUTH_PREFIX}{backend_key}_KEY')
    client_secret = getattr(settings, f'{SOCIAL_AUTH_PREFIX}{backend_key}_SECRET')
    if not all([client_id, client_secret]):
        raise ValueError('OAuth client key and secret are required')

    payload = None
    redirect_uri = backend_cfg['auth_params']['redirect_uri']
    
    if backend == 'google-oauth2':
        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'access_type': backend_cfg['auth_params']['access_type'],
            'include_granted_scopes': backend_cfg['auth_params']['include_granted_scopes'],
            'grant_type': 'authorization_code',
        }
    elif backend == 'facebook':
        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
    elif backend == 'linkedin-oauth2':
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }

    return payload


def get_access_token_from_code(backend, code):
    """Get access token for any OAuth backend from code"""

    url = OAUTH_CFGS[backend]['token_url']
    payload = get_payload(backend, code)

    # different providers have different responses to their oauth endpoint
    is_post = backend != 'facebook'
    response = get_social_response(url, payload, is_post=is_post)
    return response['access_token'], response
        

def get_social_response(url, payload, is_post=True):
    if is_post:
        r = requests.post(url, data=payload)
    else:
        r = requests.get(url, params=payload)
    if r.status_code < 200 or r.status_code >= 400:
        raise ValueError(r.content)
    try:
        return r.json()
    except ValueError:
        return parse_qs(r.text)
