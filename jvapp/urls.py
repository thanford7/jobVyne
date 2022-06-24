from django.urls import path, re_path

from . import views
from jvapp.apis import auth, user

apiPath = 'api/v1/'

urlpatterns = [
    path('', views.index, name='index'),

    # Data
    re_path(apiPath + 'user/(?P<userId>[0-9]+)?/?$', user.UserView.as_view()),

    # Auth
    path(apiPath + 'auth/login/', auth.LoginView.as_view()),
    path(apiPath + 'auth/login-set-cookie/', auth.LoginSetCookieView.as_view()),
    path(apiPath + 'auth/logout/', auth.LogoutView.as_view()),
]