import { boot } from 'quasar/wrappers'
import dataUtil from 'src/utils/data'
import { getAjaxFormData } from 'src/utils/requests'

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

      return { path: redirectPageUrl || '/dashboard', query: redirectParams }
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
      if (!isAuthenticated && !to.meta.isNoAuth) {
        // redirect the user to the login page
        return { name: 'login' }
      }
      if (to.meta.userTypeBits && !(to.meta.userTypeBits & user.user_type_bits)) {
        return { name: 'dashboard' }
      }
    } catch (e) {
      return { name: 'error' }
    }
  })
})
