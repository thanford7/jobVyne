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
      { path: '', name: 'landing', meta: { isNoAuth: true }, component: () => import('pages/IndexPage.vue') },
      {
        path: 'terms-of-service',
        name: 'tos',
        meta: { isNoAuth: true },
        component: () => import('pages/TermsOfServicePage.vue')
      },
      { path: 'privacy', name: 'privacy', meta: { isNoAuth: true }, component: () => import('pages/PrivacyPage.vue') },
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
      { path: '', name: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { path: 'links', name: 'dashboard-links', component: () => import('pages/ReferralLinksPage.vue') }
    ]
  },

  {
    path: '/jobs-link/:filterId',
    name: 'jobs-link',
    meta: { isNoAuth: true },
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
