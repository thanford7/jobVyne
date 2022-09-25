from django.urls import path, re_path

from jvapp.apis import admin, ats, auth, content, currency, data, employer, job_seeker, social, stripe, tracking, user, \
    waitlist

api_path = 'api/v1/'

urlpatterns = [
    # General Data
    re_path('^admin/employer/(?P<employer_id>[0-9]+)?/?$', admin.EmployerView.as_view()),
    path('currency/', currency.CurrencyView.as_view()),
    path('employee-questions/', user.UserEmployeeProfileQuestionsView.as_view()),
    path('employer-from-domain/', employer.EmployerFromDomainView.as_view()),
    re_path('^employer/(?P<employer_id>[0-9]+)?/?$', employer.EmployerView.as_view()),
    re_path('^employer/ats/(?P<ats_id>[0-9]+)?/?$', employer.EmployerAtsView.as_view()),
    re_path('^employer/billing/(?P<employer_id>[0-9]+)?/?$', employer.EmployerBillingView.as_view()),
    path('employer/bonus/default/', employer.EmployerBonusDefaultView.as_view()),
    re_path('^employer/bonus/rule/(?P<rule_id>[0-9]+)?/?$', employer.EmployerBonusRuleView.as_view()),
    path('employer/bonus/rule/order/', employer.EmployerBonusRuleOrderView.as_view()),
    re_path('^employer/file/(?P<file_id>[0-9]+)?/?$', employer.EmployerFileView.as_view()),
    re_path('^employer/file-tag/(?P<tag_id>[0-9]+)?/?$', employer.EmployerFileTagView.as_view()),
    re_path('^employer/job/(?P<employer_job_id>[0-9]+)?/?$', employer.EmployerJobView.as_view()),
    path('employer/job/location/', employer.EmployerJobLocationView.as_view()),
    path('employer/page/', employer.EmployerPageView.as_view()),
    re_path('^employer/permission/(?P<auth_group_id>[0-9]+)?/?$', employer.EmployerAuthGroupView.as_view()),
    path('employer/user/approve/', employer.EmployerUserApproveView.as_view()),
    re_path('^employer/user/(?P<user_id>[0-9]+)?/?$', employer.EmployerUserView.as_view()),
    path('employer/user/activate/', employer.EmployerUserActivateView.as_view()),
    path('feedback/', user.FeedbackView.as_view()),
    re_path('^job-application/(?P<application_id>[0-9]+)?/?$', job_seeker.ApplicationView.as_view()),
    path('page-view/', tracking.PageTrackView.as_view()),
    re_path('^social-content-item/(?P<item_id>[0-9]+)?/?$', content.SocialContentItemView.as_view()),
    re_path('^social-link-filter/(?P<link_filter_id>\S+)?/?$', social.SocialLinkFilterView.as_view()),
    re_path('^social-link-jobs/(?P<link_filter_id>\S+)/?$', social.SocialLinkJobsView.as_view()),
    path('social-platform/', social.SocialPlatformView.as_view()),
    re_path('^social-post/(?P<post_id>[0-9]+)?/?$', content.SocialPostView.as_view()),
    path('social-post/share/', content.ShareSocialPostView.as_view()),
    re_path('^user/(?P<user_id>[0-9]+)?/?$', user.UserView.as_view()),
    re_path('^user/profile/(?P<user_id>[0-9]+)/?$', user.UserProfileView.as_view()),
    re_path('^user/file/(?P<file_id>[0-9]+)?/?$', user.UserFileView.as_view()),
    path('user/social-credentials/', user.UserSocialCredentialsView.as_view()),
    path('waitlist/', waitlist.WaitlistView.as_view()),
    
    # Chart Data
    path('data/link-performance/', data.DataLinkPerformanceView.as_view()),
    
    # ATS operations
    path('ats/custom-fields/', ats.AtsCustomFieldsView.as_view()),
    path('ats/jobs/', ats.AtsJobsView.as_view()),
    path('ats/stages/', ats.AtsStagesView.as_view()),
    
    # Billing
    path('billing/customer/', stripe.StripeProductView.as_view()),
    path('billing/product/', stripe.StripeProductView.as_view()),

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