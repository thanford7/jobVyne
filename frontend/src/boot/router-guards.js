import { boot } from 'quasar/wrappers'
import dataUtil from 'src/utils/data'

export default boot(({ app, router, store }) => {
  router.beforeEach(async (to, from) => {
    const resp = await app.config.globalProperties.$api.get('auth/check-auth/')
    const isAuthenticated = resp.data && !dataUtil.isEmptyOrNil(resp.data)
    if (!isAuthenticated && !to.meta.isNoAuth) {
      // redirect the user to the login page
      return { name: 'login' }
    }
  })
})
