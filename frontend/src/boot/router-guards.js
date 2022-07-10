import { boot } from 'quasar/wrappers'
import dataUtil from 'src/utils/data'
import { getAjaxFormData } from 'src/utils/requests'

export default boot(({ app, router }) => {
  router.beforeEach(async (to, from) => {
    const $api = app.config.globalProperties.$api
    if (to.name === 'auth-callback') {
      const provider = to.params.provider
      const protectedParams = ['code', 'state']
      try {
        // The redirect URL needs to be the same as the one passed to the social platform
        // The platform adds a few additional params so we need to remove them
        let redirectUrl = window.location.origin + to.fullPath.replace(to.hash, '')
        redirectUrl = dataUtil.removeQueryParams(redirectUrl, protectedParams)
        await $api.post(
          `/social/${provider}/`,
          getAjaxFormData({
            code: to.query.code,
            redirectUrl
          })
        )
      } catch (e) {
        return { name: 'error' }
      }
      return {
        name: to.query.redirectPage || 'dashboard',
        query: dataUtil.omit(to.query, [...protectedParams, 'redirectPage'])
      }
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
