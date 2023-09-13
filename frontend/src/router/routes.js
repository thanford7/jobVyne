import { USER_TYPES } from 'src/utils/user-types'

const routes = [
  {
    path: '/',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: 'login', name: 'login', meta: { isNoAuth: true }, component: () => import('pages/auth/LoginPage.vue') },
      { path: '', name: 'home', meta: { isNoAuth: true }, component: () => import('pages/auth/LoginPage.vue') },
      {
        // This is a "fake" page. We need a route to catch the redirect after social authentication
        // This route is redirected in router-guard.js
        path: '/auth/:provider/callback',
        name: 'auth-callback',
        meta: { isNoAuth: true },
        component: () => {}
      }
    ]
  },

  {
    path: '/password-reset-generate',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'password-reset-generate', meta: { isNoAuth: true }, component: () => import('pages/auth/GenerateResetPasswordPage.vue') }
    ]
  },

  {
    path: '/password-reset/:uid(\\S+)/:token(\\S+)',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'password-reset', meta: { isNoAuth: true }, component: () => import('pages/auth/ResetPasswordPage.vue') }
    ]
  },

  {
    path: '/verify-email/:uid(\\S+)/:token(\\S+)',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'verify-email', meta: { isNoAuth: true }, component: () => import('pages/auth/VerifyEmailPage.vue') }
    ]
  },

  {
    path: '/onboard',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'onboard', component: () => import('pages/onboard-page/OnboardPage.vue') }
    ]
  },

  {
    path: '/',
    component: () => import('layouts/LandingLayout.vue'),
    children: [
      {
        path: 'terms-of-service',
        name: 'tos',
        meta: { isNoAuth: true },
        component: () => import('pages/TermsOfServicePage.vue')
      },
      { path: 'privacy', name: 'privacy', meta: { isNoAuth: true }, component: () => import('pages/PrivacyPage.vue') },
      { path: 'credits', name: 'credits', meta: { isNoAuth: true }, component: () => import('pages/CreditsPage.vue') }
    ]
  },

  {
    path: '/:namespace(admin)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        meta: { userTypeBits: USER_TYPES.Admin },
        component: () => import('pages/admin/DashboardPage.vue')
      },
      {
        path: 'users',
        name: 'admin-users',
        meta: { userTypeBits: USER_TYPES.Admin },
        component: () => import('pages/admin/UsersPage.vue')
      },
      {
        path: 'employers',
        name: 'admin-employers',
        meta: { userTypeBits: USER_TYPES.Admin },
        component: () => import('pages/admin/EmployersPage.vue')
      },
      {
        path: 'user-jobs',
        name: 'admin-user-jobs',
        meta: { userTypeBits: USER_TYPES.Admin },
        component: () => import('pages/admin/user-jobs-page/UserJobsPage.vue')
      },
      {
        path: 'scrapers',
        name: 'admin-scrapers',
        meta: { userTypeBits: USER_TYPES.Admin },
        component: () => import('pages/admin/JobScrapersPage.vue')
      }
    ]
  },

  {
    path: '/:namespace(candidate)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: 'job-applications',
        name: 'candidate-dashboard',
        meta: { userTypeBits: USER_TYPES.Candidate },
        component: () => import('pages/candidate/DashboardPage.vue')
      },
      {
        path: 'favorites',
        name: 'candidate-favorites',
        meta: { userTypeBits: USER_TYPES.Candidate },
        component: () => import('pages/candidate/FavoritesPage.vue')
      },
      {
        path: 'connections',
        name: 'candidate-connections',
        meta: { userTypeBits: USER_TYPES.Candidate },
        component: () => import('pages/candidate/ConnectionsPage.vue')
      }
    ]
  },

  {
    path: '/:namespace(employee)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'employee-dashboard',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/DashboardPage.vue')
      },
      {
        path: ':key(employee-jobs)',
        name: 'employee-jobs',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/JobsPage.vue')
      },
      {
        path: ':key(employee-applications)',
        name: 'employee-applications',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/ApplicationsPage.vue')
      },
      {
        path: ':key(employee-profile-page)',
        name: 'employee-profile-page',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/ProfilePage.vue')
      },
      {
        path: ':key(employee-social)',
        name: 'employee-social',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/social-page/SocialPage.vue')
      }
    ]
  },

  {
    path: '/:namespace(influencer)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'influencer-dashboard',
        meta: { userTypeBits: USER_TYPES.Influencer },
        component: () => import('pages/DashboardPage.vue')
      },
      {
        path: 'jobs',
        name: 'influencer-jobs',
        meta: { userTypeBits: USER_TYPES.Influencer },
        component: () => import('pages/influencer/JobBoardsPage.vue')
      },
      {
        path: ':key(influencer-social)',
        name: 'influencer-social',
        meta: { userTypeBits: USER_TYPES.Influencer },
        component: () => import('pages/influencer/social-page/SocialPage.vue')
      }
    ]
  },

  {
    path: '/:namespace(employer)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'employer-dashboard',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/dashboard-page/DashboardPage.vue')
      },
      {
        path: ':key(employer-jobs)',
        name: 'employer-jobs',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/jobs-page/JobsPage.vue')
      },
      {
        path: ':key(employer-job-ads)',
        name: 'employer-job-ads',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/job-add-page/JobAddPage.vue')
      },
      {
        path: ':key(employer-job-boards)',
        name: 'employer-job-boards',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/job-boards-page/JobBoardsPage.vue')
      },
      {
        path: ':key(employer-referrals)',
        name: 'employer-referrals',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/referrals-page/ReferralsPage.vue')
      },
      {
        path: ':key(employer-applications)',
        name: 'employer-applications',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/applications-page/ApplicationsPage.vue')
      },
      {
        path: ':key(employer-user-management)',
        name: 'employer-user-management',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/user-management-page/UserManagementPage.vue')
      },
      {
        path: ':key(employer-settings)',
        name: 'employer-settings',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/settings-page/SettingsPage.vue')
      }
    ]
  },

  {
    path: '/:namespace(account)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: ':key(settings)',
        name: 'settings',
        component: () => import('pages/settings-page/AccountSettingsPage.vue')
      },
      {
        path: ':key(feedback)',
        name: 'feedback',
        component: () => import('pages/feedback-page/FeedbackPage.vue')
      }
    ]
  },

  {
    path: '/jobs-link/:filterId',
    name: 'jobs-link',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/job/:jobKey',
    name: 'job',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/jobs',
    name: 'jobs',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/group/:employerKey',
    name: 'group',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/co/:employerKey',
    name: 'company',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/profession/:professionKey',
    name: 'profession',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/jv/:userKey',
    name: 'profile',
    meta: { isNoAuth: true, trackRoute: true },
    component: () => import('layouts/JobsLayout.vue')
  },

  {
    path: '/:namespace(karma)',
    component: () => import('layouts/BodyLeftDrawerFooterLayout.vue'),
    children: [
      {
        path: '',
        name: 'karma-home',
        meta: {},
        component: () => import('pages/karma/home-page/HomePage.vue')
      },
      {
        path: 'intro-request/:requestId',
        name: 'intro-request',
        meta: { isNoAuth: true, trackRoute: true },
        component: () => import('pages/karma/intro-request-page/IntroRequestPage.vue')
      },
      {
        path: 'connect-request/:requestId',
        name: 'connect-request',
        meta: { isNoAuth: true, trackRoute: true },
        component: () => import('pages/karma/connection-request-page/ConnectionRequestPage.vue')
      },
      {
        // This is a "fake" page. We need a route to catch the redirect after a user donates
        // This route is redirected in router-guard.js
        path: 'donation-confirm',
        name: 'donation-confirm',
        meta: {},
        component: () => {}
      }
    ]
  },

  {
    path: '/unsubscribe',
    name: 'unsubscribe',
    meta: { isNoAuth: true },
    component: () => import('pages/UnsubscribePage.vue')
  },

  {
    path: '/error',
    name: 'error',
    meta: { isNoAuth: true },
    component: () => import('pages/ErrorPage.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    meta: { isNoAuth: true },
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
