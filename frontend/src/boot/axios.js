import { boot } from 'quasar/wrappers'
import { Cookies } from 'quasar'
import axios from 'axios'
import emitter from 'tiny-emitter/instance'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
export const AJAX_EVENTS = {
  ERROR: 'ajax-error',
  SUCCESS: 'ajax-success'
}

axios.defaults.withCredentials = true
export default boot(({ app, ssrContext, store, router }) => {
  const api = axios.create({
    withCredentials: true,
    baseURL: process.env.API_URL,
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

  api.interceptors.response.use(function (response) {
    const successMessage = response?.data?.successMessage
    if (successMessage) {
      emitter.emit(AJAX_EVENTS.SUCCESS, successMessage)
    }
    return response
  }, function (error) {
    emitter.emit(AJAX_EVENTS.ERROR, error)
    return Promise.reject(error)
  })

  // for use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  const emitterEvents = {
    $on: (...args) => emitter.on(...args),
    $once: (...args) => emitter.once(...args),
    $off: (...args) => emitter.off(...args),
    $emit: (...args) => emitter.emit(...args)
  }

  app.config.globalProperties.$api = api
  store.use(() => {
    return { $api: api, $router: router, ...emitterEvents }
  })
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API

  app.config.globalProperties.$global = emitterEvents
})
