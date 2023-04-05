from django.db.models import Q
from django.shortcuts import redirect
from social_core.backends.google import GoogleOAuth2
from social_core.backends.linkedin import LinkedinOAuth2

from jvapp.apis.auth import get_token_expiration_dt, update_all_social_creds
from jvapp.models import JobVyneUser
from jvapp.models.user import UserSocialCredential

USER_FIELDS = ['username', 'email', 'user_type_bits']


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}
    
    fields = {name: kwargs.get(name, details.get(name))
              for name in backend.setting('USER_FIELDS', USER_FIELDS)}
    if not fields:
        return
    
    return {
        'is_new': True,
        'user': strategy.create_user(**fields, is_email_verified=True)
    }


def save_user_credentials(strategy, details, backend, user=None, *args, **kwargs):
    provider = backend.name
    access_token = kwargs['response']['access_token']
    expiration_seconds = kwargs['response'].get('expires_in')
    expiration_dt = get_token_expiration_dt(expiration_seconds) if expiration_seconds else None
    email = details['email']
    user_filter = Q(email=email) | Q(business_email=email)
    users = JobVyneUser.objects.prefetch_related('social_credential').filter(user_filter)
    for jv_user in users:
        social_credential = next(
            (
                sc for sc in jv_user.social_credential.all()
                if sc.provider == provider and sc.email == email
            ),
            None
        )
        if not social_credential:
            UserSocialCredential(
                user=jv_user,
                access_token=access_token,
                provider=provider,
                email=email,
                expiration_dt=expiration_dt
            ).save()

    update_all_social_creds(user, provider, email, access_token, expiration_dt)


def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    if (
        backend.name == 'google-oauth2' and social
        and response.get('refresh_token') is None
        and social.extra_data.get('refresh_token') is None
    ):
        return redirect('/login/google-oauth2?approval_prompt=force')
    
    
class CustomGoogleOAuth2(GoogleOAuth2):

    def get_scope(self):
        scope = super(GoogleOAuth2, self).get_scope()
        if not self.data.get('isLogin'):
            scope = scope + ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']
        return scope
    
    
class CustomLinkedinOAuth2(LinkedinOAuth2):

    def get_scope(self):
        scope = super(LinkedinOAuth2, self).get_scope()
        if not self.data.get('isLogin'):
            scope = scope + ['w_member_social']
        return scope
