import { boot } from 'quasar/wrappers'
import { Cookies } from 'quasar'
import axios from 'axios'
import emitter from 'tiny-emitter/instance'
import md5 from 'md5'
import { setupCache, serializeQuery } from 'axios-cache-adapter'

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

// https://github.com/RasCarlito/axios-cache-adapter/issues/231
const { adapter: axiosCacheAdapter, cache } = setupCache({
  // debug: process.env.NODE_ENV !== 'production',
  debug: false,
  maxAge: 1000 // In milliseconds
})

const runningRequests = {}
const noDuplicateRequestsAdapter = request => {
  const requestUrl = `${request.baseURL ? request.baseURL : ''}${request.url}`
  let requestKey = requestUrl + serializeQuery(request)

  if (request.data) requestKey = requestKey + md5(request.data)

  // Add the request to runningRequests
  if (!runningRequests[requestKey]) runningRequests[requestKey] = axiosCacheAdapter(request)

  // Return the response promise
  return runningRequests[requestKey].finally(() => {
    // Finally, delete the request from the runningRequests whether there's error or not
    delete runningRequests[requestKey]
  })
}

axios.defaults.withCredentials = true
export default boot(({ app, ssrContext, store, router }) => {
  const api = axios.create({
    withCredentials: true,
    baseURL: process.env.API_URL,
    adapter: noDuplicateRequestsAdapter,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })

  api.cache = cache

  api.interceptors.request.use(function (config) {
    const cookies = process.env.SERVER
      ? Cookies.parseSSR(ssrContext)
      : Cookies // otherwise we're on client
    config.headers['X-CSRFTOKEN'] = cookies.get('csrftoken')
    return config
  }, (error) => {
    return Promise.reject(error)
  })

  api.interceptors.response.use(function (response) {
    const successMessage = response?.data?.successMessage
    const errorMessages = response?.data?.errorMessages
    if (successMessage) {
      emitter.emit(AJAX_EVENTS.SUCCESS, successMessage)
    }
    if (errorMessages && errorMessages.length) {
      errorMessages.forEach((errorMsg) => {
        emitter.emit(AJAX_EVENTS.ERROR, { message: errorMsg })
      })
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
