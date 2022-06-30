from django.urls import path, re_path

from . import views
from jvapp.apis import auth, user

apiPath = 'api/v1/'

urlpatterns = [
    # Data
    re_path('user/(?P<userId>[0-9]+)?/?$', user.UserView.as_view()),

    # Auth
    path('auth/login/', auth.LoginView.as_view()),
    path('auth/login-set-cookie/', auth.LoginSetCookieView.as_view()),
    path('auth/logout/', auth.LogoutView.as_view()),
    
    # Social auth
    path('social/<backend>/', auth.social_auth),
    path('social-credentials/', auth.SocialAuthCredentialsView.as_view())
]

handler404 = 'jvapp.views.handler404'
handler500 = 'jvapp.views.handler500'