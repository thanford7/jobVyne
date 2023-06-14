from django.urls import path, re_path

from jvapp.apis import (
    admin, ats, auth, content, currency, data, donation_org, email, employer, job_seeker, job, jobs, job_subscription,
    karma, message, notification, sales, slack, social, stripe, test, tracking, user
)
from jvapp.apis.geocoding import LocationSearchView

urlpatterns = [
    # General Data
    path('admin/ats-failure/', admin.AdminAtsFailureView.as_view()),
    path('admin/ats-jobs/', admin.AdminAtsJobsView.as_view()),
    re_path('^admin/employer/(?P<employer_id>[0-9]+)?/?$', admin.AdminEmployerView.as_view()),
    path('admin/job-scraper/', admin.AdminJobScrapersView.as_view()),
    re_path('^admin/user/(?P<user_id>[0-9]+)?/?$', admin.AdminUserView.as_view()),
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
    re_path('^employer/job-application/(?P<application_id>[0-9]+)?/?$', employer.EmployerJobApplicationView.as_view()),
    path('employer/job-application-requirement/', employer.EmployerJobApplicationRequirementView.as_view()),
    path('employer/job/bonus/', employer.EmployerJobBonusView.as_view()),
    path('employer/job/department/', employer.EmployerJobDepartmentView.as_view()),
    path('employer/job/location/', employer.EmployerJobLocationView.as_view()),
    re_path('^employer/permission/(?P<auth_group_id>[0-9]+)?/?$', employer.EmployerAuthGroupView.as_view()),
    path('employer/referral/request/', employer.EmployerReferralRequestView.as_view()),
    re_path('^employer/slack/(?P<slack_cfg_id>[0-9]+)?/?$', employer.EmployerSlackView.as_view()),
    re_path('^employer/subscription/(?P<employer_id>[0-9]+)?/?$', employer.EmployerSubscriptionView.as_view()),
    path('employer/user/approve/', employer.EmployerUserApproveView.as_view()),
    re_path('^employer/user/(?P<user_id>[0-9]+)?/?$', employer.EmployerUserView.as_view()),
    path('employer/user/activate/', employer.EmployerUserActivateView.as_view()),
    path('employer/user/upload/', employer.EmployerUserUploadView.as_view()),
    path('feedback/', user.FeedbackView.as_view()),
    re_path('^job-application/(?P<application_id>[0-9]+)?/?$', job_seeker.ApplicationView.as_view()),
    path('job-application/external/', job_seeker.ApplicationExternalView.as_view()),
    path('job/department/', job.JobDepartmentView.as_view()),
    path('job/location/', job.LocationView.as_view()),
    path('jobs/', jobs.JobsView.as_view()),
    re_path('^job-subscription/(?P<subscription_id>[0-9]+)?/?$', job_subscription.JobSubscriptionView.as_view()),
    path('notification-preference/', notification.UserNotificationPreferenceView.as_view()),
    path('page-view/', tracking.PageTrackView.as_view()),
    re_path('^social-content-item/(?P<item_id>[0-9]+)?/?$', content.SocialContentItemView.as_view()),
    path('social-link/share/', social.ShareSocialLinkView.as_view()),
    re_path('^social-link/(?P<link_id>\S+)?/?$', social.SocialLinkView.as_view()),
    re_path('^social-link-jobs/(?P<link_id>\S+)?/?$', social.SocialLinkJobsView.as_view()),
    path('social-link-post-jobs/', social.SocialLinkPostJobsView.as_view()),
    path('social-platform/', social.SocialPlatformView.as_view()),
    re_path('^social-post/(?P<post_id>[0-9]+)?/?$', content.SocialPostView.as_view()),
    path('social-post/share/', content.ShareSocialPostView.as_view()),
    re_path('^user/(?P<user_id>[0-9]+)?/?$', user.UserView.as_view()),
    re_path('^user/employee-checklist/(?P<user_id>[0-9]+)?/?$', user.UserEmployeeChecklistView.as_view()),
    re_path('^user/profile/(?P<user_id>[0-9]+)/?$', user.UserProfileView.as_view()),
    re_path('^user/file/(?P<file_id>[0-9]+)?/?$', user.UserFileView.as_view()),
    path('user/job-application-review/', user.UserJobApplicationReviewView.as_view()),
    path('user/social-credentials/', user.UserSocialCredentialsView.as_view()),
    
    # Karma
    path('karma/connection-donation-organization/', karma.UserRequestDonationOrgView.as_view()),
    path('karma/donation-organization/', karma.DonationOrganizationView.as_view()),
    path('karma/user/', karma.UserView.as_view()),
    path('karma/user-donation/', karma.UserDonationView.as_view()),
    path('karma/user-donation-organization/', karma.UserDonationOrganizationView.as_view()),
    path('karma/user-request/', karma.UserRequestView.as_view()),
    
    # Emails
    path('email/admin/', notification.MessageAdminView.as_view()),
    path('email/employer/applicant/', notification.MessageEmployerApplicantView.as_view()),
    path('email/employer/employee/', notification.MessageEmployerEmployeeView.as_view()),
    path('gmail/webhooks/inbound/', email.GmailInboundView.as_view()),
    
    # Sales
    path('sales/inquiry/', sales.SalesInquiryView.as_view()),
    path('sales/waitlist/', sales.WaitlistView.as_view()),
    
    # Chart Data
    path('data/applications/', data.ApplicationsView.as_view()),
    path('data/page-views/', data.PageViewsView.as_view()),
    
    # ATS operations
    path('ats/custom-fields/', ats.AtsCustomFieldsView.as_view()),
    path('ats/jobs/', ats.AtsJobsView.as_view()),
    path('ats/stages/', ats.AtsStagesView.as_view()),
    path('lever/oauth-token/', ats.LeverOauthTokenView.as_view()),
    path('lever/oauth-url/', ats.LeverOauthUrlView.as_view()),
    re_path('^lever/webhooks/(?P<employer_id>[0-9]+)?/?$', ats.LeverWebhooksView.as_view()),
    
    # Billing
    path('billing/charge/', stripe.StripeChargeView.as_view()),
    re_path('^billing/payment-method/(?P<payment_method_id>\S+)?/?$', stripe.StripePaymentMethodView.as_view()),
    path('billing/invoice/', stripe.StripeInvoiceView.as_view()),
    path('billing/invoice-pay/', stripe.StripePayInvoiceView.as_view()),
    path('billing/product/', stripe.StripeProductView.as_view()),
    path('billing/test-status/', stripe.StripeTestStatus.as_view()),
    path('billing/setup/', stripe.StripeSetupIntentView.as_view()),
    re_path('^billing/subscription/((?P<subscription_id>\S+)/)?$', stripe.StripeSubscriptionView.as_view()),
    path('billing/webhooks/', stripe.StripeWebhooksView.as_view()),

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
    
    # Google
    path('search/location/', LocationSearchView.as_view()),
    
    # Every.org
    path('search/donation-org/', donation_org.DonationOrgSearchView.as_view()),
    
    # Sendgrid email
    path('sendgrid/webhooks/', email.SendgridWebhooksView.as_view()),
    path('sendgrid/webhooks/inbound/', email.SendgridWebhooksInboundView.as_view()),
    
    # Slack
    path('slack/channel/', slack.SlackChannelView.as_view()),
    path('slack/command/suggest/', slack.SlackCommandSuggestView.as_view()),
    path('slack/message/job/', slack.SlackJobsMessageView.as_view()),
    path('slack/message/referral/', slack.SlackReferralsMessageView.as_view()),
    path('slack/webhooks/inbound/', slack.SlackWebhookInboundView.as_view()),
    
    # Twilio SMS
    path('twilio/webhooks/', message.TwilioWebhooksView.as_view()),
    
    # Social auth
    path('social/slack/', auth.social_auth_slack),
    path('social/calendly/', auth.social_auth_calendly),
    path('social/<backend>/', auth.social_auth),
    path('social-credentials/', auth.SocialAuthCredentialsView.as_view()),
    
    # Test url
    path('test/email/', test.TestEmailView.as_view()),
    path('test/error-msg/', test.TestErrorView.as_view())
]

handler404 = 'jvapp.views.handler404'
handler500 = 'jvapp.views.handler500'
