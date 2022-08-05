import { boot } from 'quasar/wrappers'
import dataUtil from 'src/utils/data'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData } from 'src/utils/requests'

const isMainPageFn = (to) => {
  if (!to) {
    return false
  }
  const mainPageNamespaces = ['candidate', 'employee', 'influencer', 'employer', 'user']
  return to.params.namespace && mainPageNamespaces.includes(to.params.namespace)
}

export default boot(({ app, router }) => {
  router.beforeEach(async (to, from) => {
    const $api = app.config.globalProperties.$api
    // Handle oauth callback
    if (to.name === 'auth-callback') {
      const provider = to.params.provider
      const { state, redirectPageUrl, redirectParams, userTypeBit } = JSON.parse(to.query.state)
      try {
        await $api.post(
          `/social/${provider}/`,
          getAjaxFormData({ code: to.query.code, state, userTypeBit })
        )
      } catch (e) {
        return { name: 'error' }
      }

      return { path: redirectPageUrl || '/user/profile', query: redirectParams }
    }

    // Capture page view
    if (to.meta.trackRoute) {
      $api.post('/page-view/', getAjaxFormData({
        relative_url: to.path,
        filter_id: to.params.filterId
      }))
    }

    // Redirect if user doesn't have access to a specific page
    try {
      const resp = await $api.get('auth/check-auth/')
      const user = resp.data
      const isAuthenticated = user && !dataUtil.isEmptyOrNil(user)

      const isMainPage = isMainPageFn(to)
      const isOnboardingNeeded = isAuthenticated && !user.user_type_bits
      if (isOnboardingNeeded && isMainPage) {
        return { name: 'onboard' }
      }

      if (!isAuthenticated && !to.meta.isNoAuth) {
        // redirect the user to the login page
        return { name: 'login' }
      }

      const { canView, canEdit } = pagePermissionsUtil.getUserPagePermissions(user, to.name)

      // Redirect user to page where they can verify their email if they haven't already
      if (!canView) {
        return { name: 'profile', params: { namespace: 'user', key: 'profile' }, query: { tab: 'security' } }
      }

      // Add meta permission to edit which can be used by the page
      to.meta.canEdit = canEdit
    } catch (e) {
      return { name: 'error' }
    }
  })
})
