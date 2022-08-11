from django.urls import path, re_path

from jvapp.apis import auth, employer, job_seeker, social, tracking, user, waitlist

api_path = 'api/v1/'

urlpatterns = [
    # Data
    path('employer-from-domain/', employer.EmployerFromDomainView.as_view()),
    re_path('^employer/(?P<employer_id>[0-9]+)?/?$', employer.EmployerView.as_view()),
    re_path('^employer/file/(?P<file_id>[0-9]+)?/?$', employer.EmployerFileView.as_view()),
    re_path('^employer/file-tag/(?P<tag_id>[0-9]+)?/?$', employer.EmployerFileTagView.as_view()),
    re_path('^employer/job/(?P<employer_job_id>[0-9]+)?/?$', employer.EmployerJobView.as_view()),
    path('employer/job/location/', employer.EmployerJobLocationView.as_view()),
    path('employer/page/', employer.EmployerPageView.as_view()),
    re_path('^employer/permission/(?P<auth_group_id>[0-9]+)?/?$', employer.EmployerAuthGroupView.as_view()),
    path('employer/user/approve/', employer.EmployerUserApproveView.as_view()),
    re_path('^employer/user/(?P<user_id>[0-9]+)?/?$', employer.EmployerUserView.as_view()),
    path('employer/user/activate/', employer.EmployerUserActivateView.as_view()),
    re_path('^job-application/(?P<application_id>[0-9]+)?/?$', job_seeker.ApplicationView.as_view()),
    path('page-view/', tracking.PageTrackView.as_view()),
    re_path('^social-link-filter/(?P<link_filter_id>\S+)?/?$', social.SocialLinkFilterView.as_view()),
    re_path('^social-link-jobs/(?P<link_filter_id>\S+)/?$', social.SocialLinkJobsView.as_view()),
    path('social-platform/', social.SocialPlatformView.as_view()),
    re_path('^user/(?P<user_id>[0-9]+)?/?$', user.UserView.as_view()),
    path('waitlist/', waitlist.WaitlistView.as_view()),

    # Auth
    path('auth/login/', auth.LoginView.as_view()),
    path('auth/login-set-cookie/', auth.LoginSetCookieView.as_view()),
    path('auth/logout/', auth.LogoutView.as_view()),
    path('auth/check-auth/', auth.CheckAuthView.as_view()),
    path('auth/validate-captcha/', auth.validate_recaptcha),
    
    # Password (re)set
    path('password-reset/', auth.PasswordResetView.as_view()),
    path('password-reset-generate/', auth.PasswordResetGenerateView.as_view()),
    path('password-reset-from-email/', auth.PasswordResetFromEmailView.as_view()),
    
    # Email verification
    path('verify-email-generate/', user.UserEmailVerificationGenerateView.as_view()),
    path('verify-email/', user.UserEmailVerificationView.as_view()),
    
    # Social auth
    path('social/<backend>/', auth.social_auth),
    path('social-credentials/', auth.SocialAuthCredentialsView.as_view())
]

handler404 = 'jvapp.views.handler404'
handler500 = 'jvapp.views.handler500'