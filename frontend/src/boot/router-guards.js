import { boot } from 'quasar/wrappers'
import dataUtil from 'src/utils/data'
import { getAjaxFormData } from 'src/utils/requests'

export default boot(({ app, router }) => {
  router.beforeEach(async (to, from) => {
    const $api = app.config.globalProperties.$api
    if (to.name === 'auth-callback') {
      const provider = to.params.provider
      const { state, redirectPageUrl, redirectParams } = JSON.parse(to.query.state)
      try {
        await $api.post(
          `/social/${provider}/`,
          getAjaxFormData({ code: to.query.code, state })
        )
      } catch (e) {
        return { name: 'error' }
      }

      return { path: redirectPageUrl || '/dashboard', query: redirectParams }
    }

    try {
      const resp = await $api.get('auth/check-auth/')
      const isAuthenticated = resp.data && !dataUtil.isEmptyOrNil(resp.data)
      if (!isAuthenticated && !to.meta.isNoAuth) {
        // redirect the user to the login page
        return { name: 'login' }
      }
    } catch (e) {
      return { name: 'error' }
    }
  })
})
