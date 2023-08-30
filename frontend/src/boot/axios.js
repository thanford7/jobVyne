import { boot } from 'quasar/wrappers'
import axios from 'axios'
import dateTimeUtil from 'src/utils/datetime.js'
import { getCsrfToken } from 'src/utils/requests.js'
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
  WARNING: 'ajax-warning',
  SUCCESS: 'ajax-success'
}

const CODE_VERSION_KEY = 'jv-version'
const RELOAD_FLAG_KEY = 'jv-reload'

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
    config.headers['X-CSRFTOKEN'] = getCsrfToken(ssrContext)
    return config
  }, (error) => {
    return Promise.reject(error)
  })

  api.interceptors.response.use(function (response) {
    const codeVersion = response.headers[CODE_VERSION_KEY] || 'default'
    const localCodeVersion = localStorage.getItem(CODE_VERSION_KEY)
    let timeDiffMin = 0
    if ((codeVersion !== 'default') && localCodeVersion) {
      const codeVersionDt = dateTimeUtil.forceToDate(codeVersion)
      const localCodeVersionDt = dateTimeUtil.forceToDate(localCodeVersion)
      timeDiffMin = (codeVersionDt - localCodeVersionDt) / (1000 * 60)
    }
    const hasReloaded = (localStorage.getItem(RELOAD_FLAG_KEY) || 'false') === 'true'

    if (timeDiffMin > 5) {
      localStorage.setItem(CODE_VERSION_KEY, codeVersion)
      localStorage.setItem(RELOAD_FLAG_KEY, 'true')
      window.location.reload()
    }

    if (!localCodeVersion) {
      localStorage.setItem(CODE_VERSION_KEY, codeVersion)
    }

    if (hasReloaded) {
      localStorage.setItem(RELOAD_FLAG_KEY, 'false')
      emitter.emit(AJAX_EVENTS.SUCCESS, { message: 'Website has been updated. Reloaded page to get the freshest grapes 🍇' })
    }

    const successMessage = response?.data?.successMessage
    const errorMessages = response?.data?.errorMessages
    const warningMessages = response?.data?.warningMessages
    if (successMessage) {
      emitter.emit(AJAX_EVENTS.SUCCESS, { message: successMessage })
    }
    if (warningMessages && warningMessages.length) {
      warningMessages.forEach((warningMsg) => {
        emitter.emit(AJAX_EVENTS.WARNING, { message: warningMsg })
      })
    }
    if (errorMessages && errorMessages.length) {
      errorMessages.forEach((errorMsg) => {
        emitter.emit(AJAX_EVENTS.ERROR, { message: errorMsg })
      })
    }
    return response
  }, function (error) {
    emitter.emit(AJAX_EVENTS.ERROR, { error })
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

  app.config.globalProperties.$log = (txt) => {
    console.log(txt)
  }
})
