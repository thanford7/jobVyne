import { USER_TYPES } from 'src/utils/user-types'

const routes = [
  {
    path: '/login',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'login', meta: { isNoAuth: true }, component: () => import('pages/auth/LoginPage.vue') }
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
      { path: '', name: 'landing', meta: { isNoAuth: true }, component: () => import('pages/index-page/IndexPage.vue') },
      {
        path: 'terms-of-service',
        name: 'tos',
        meta: { isNoAuth: true },
        component: () => import('pages/TermsOfServicePage.vue')
      },
      { path: 'privacy', name: 'privacy', meta: { isNoAuth: true }, component: () => import('pages/PrivacyPage.vue') },
      { path: 'credits', name: 'credits', meta: { isNoAuth: true }, component: () => import('pages/CreditsPage.vue') },
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
        path: 'dashboard',
        name: 'candidate-dashboard',
        meta: { userTypeBits: USER_TYPES.Candidate },
        component: () => import('pages/candidate/DashboardPage.vue')
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
        path: ':key(employee-links)',
        name: 'employee-links',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/ReferralLinksPage.vue')
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
        path: ':key(employee-social-accounts)',
        name: 'employee-social-accounts',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/SocialAccountsPage.vue')
      },
      {
        path: ':key(employee-content)',
        name: 'employee-content',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/ContentPage.vue')
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
        path: ':key(employer-job-links)',
        name: 'employer-job-links',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/job-links-page/JobLinksPage.vue')
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
        path: ':key(employer-profile-page)',
        name: 'employer-profile-page',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/EmployerProfileCfgPage.vue')
      },
      {
        path: ':key(employer-content)',
        name: 'employer-content',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/ContentPage.vue')
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
    path: '/:namespace(user)',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: ':key(profile)',
        name: 'profile',
        component: () => import('pages/ProfilePage.vue')
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
    path: '/jobs-link/example/:employerId(\\d+)/:ownerId(\\d+)?/:tab?',
    name: 'jobs-link-example',
    meta: { isNoAuth: true, isExample: true },
    component: () => import('layouts/JobsLayout.vue')
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
