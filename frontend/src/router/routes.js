const routes = [
  {
    path: '/login',
    component: () => import('layouts/HeaderlessLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },

  {
    path: '/',
    component: () => import('layouts/UnauthenticatedLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'terms-of-service', component: () => import('pages/TermsOfServicePage.vue') },
      { path: 'privacy', component: () => import('pages/PrivacyPage.vue') },
      { path: '/auth/:provider/callback', component: () => import('pages/AuthCallbackPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
