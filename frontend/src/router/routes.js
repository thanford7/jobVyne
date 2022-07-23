import { USER_TYPES } from 'src/utils/user-types'

const routes = [
  {
    path: '/login',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', name: 'login', meta: { isNoAuth: true }, component: () => import('pages/LoginPage.vue') }
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
    path: '/dashboard',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {
        path: ':namespace(admin|candidate|employee|influencer|employer)?',
        name: 'dashboard',
        component: () => import('pages/DashboardPage.vue')
      },
      // employee pages
      {
        path: ':namespace(employee)/:key(links)',
        name: 'dashboard-links',
        meta: { userTypeBits: USER_TYPES.Employee },
        component: () => import('pages/employee/ReferralLinksPage.vue')
      },
      // employer pages
      {
        path: ':namespace(employer)/:key(user-management)',
        name: 'user-management',
        meta: { userTypeBits: USER_TYPES.Employer },
        component: () => import('pages/employer/UserManagementPage.vue')
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
