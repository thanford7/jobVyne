from django.shortcuts import redirect

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
        'user': strategy.create_user(**fields)
    }


def redirect_if_no_refresh_token(backend, response, social, *args, **kwargs):
    if (
        backend.name == 'google-oauth2' and social
        and response.get('refresh_token') is None
        and social.extra_data.get('refresh_token') is None
    ):
        return redirect('/login/google-oauth2?approval_prompt=force')
