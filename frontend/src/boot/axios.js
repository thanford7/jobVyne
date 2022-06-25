import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { Cookies } from 'quasar'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
axios.defaults.withCredentials = true
export default boot(({ app, ssrContext, store }) => {
  const api = axios.create({
    baseURL: process.env.API,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })

  api.interceptors.request.use(function (config) {
    const cookies = process.env.SERVER
      ? Cookies.parseSSR(ssrContext)
      : Cookies // otherwise we're on client
    config.headers['X-CSRFTOKEN'] = cookies.get('csrftoken')

    return config
  })

  // for use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  store.use(() => {
    return { $api: api }
  })
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})
