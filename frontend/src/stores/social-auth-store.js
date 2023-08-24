import { defineStore } from 'pinia'
import buildURL from 'axios/lib/helpers/buildURL'
import dataUtil from 'src/utils/data.js'

/*
This is the process for social authentication:
(1) User clicks button to use a social platform for authentication
(2) User is sent to the social platform's auth page
(3) User is redirected to a "fake" JobVyne auth page which is caught in router-guards
(4) The router-guard uses the credentials from the incoming url to authenticate the user
(5) The router-guard redirects the user to the ultimate page they land on
 */
const META_STRING_DELIMITER = '||'
const KEY_VAL_DELIMITER = '|'

const serializeBasicObject = (targetObj) => {
  if (!targetObj) {
    return ''
  }
  return Object.entries(targetObj).reduce((objString, [key, val]) => {
    const param = `${key}=${val || ''}`
    if (!objString.length) {
      return param
    }
    return `${objString}${KEY_VAL_DELIMITER}${param}`
  }, '')
}

const deserializeBasicObject = (targetStr) => {
  if (!targetStr) {
    return ''
  }
  const keyValPairs = targetStr.split(KEY_VAL_DELIMITER)
  return keyValPairs.reduce((targetObj, keyValPair) => {
    const splitIdx = keyValPair.indexOf('=')
    const key = keyValPair.slice(0, splitIdx)
    targetObj[key] = keyValPair.slice(splitIdx + 1, keyValPair.length)
    return targetObj
  }, {})
}

const metaDataCfg = {
  state: {},
  redirectPageUrl: {},
  redirectParams: {
    serialize: serializeBasicObject,
    deserialize: deserializeBasicObject
  },
  userTypeBit: { deserialize: Number },
  isLogin: { deserialize: dataUtil.getBoolean }
}

const getMetaString = (metaData) => {
  return Object.entries(metaDataCfg).reduce((metaString, [metaDataKey, cfg]) => {
    const val = (cfg.serialize) ? cfg.serialize(metaData[metaDataKey]) : metaData[metaDataKey]
    const param = `${metaDataKey}=${dataUtil.isNil(val) ? '' : val}`
    if (!metaString.length) {
      return param
    }
    return `${metaString}${META_STRING_DELIMITER}${param}`
  }, '')
}

export const getDataFromMetaString = (metaString) => {
  const params = metaString.split(META_STRING_DELIMITER)
  const data = params.reduce((metaData, param) => {
    const splitIdx = param.indexOf('=')
    const key = param.slice(0, splitIdx)
    let val = param.slice(splitIdx + 1, param.length)
    if (dataUtil.isNil(val) || !val.length) {
      return metaData
    }
    const deserializer = metaDataCfg[key].deserialize
    if (deserializer && val) {
      val = deserializer(val)
    }
    metaData[key] = val
    return metaData
  }, {})
  return data
}

export const useSocialAuthStore = defineStore('social-auth', {
  state: () => ({
    socialCfgs: null,
    socialCredentials: null
  }),

  actions: {
    async getOauthUrl (provider, { redirectPageUrl, redirectParams, userTypeBit, isLogin = true } = {}) {
      if (!this.socialCfgs) {
        const resp = await this.$api.get('social-credentials/')
        this.socialCfgs = resp.data
      }

      const providerCfg = this.socialCfgs[provider]
      const metaData = {
        state: providerCfg.auth_params.state,
        redirectPageUrl,
        redirectParams,
        userTypeBit,
        isLogin
      }
      const authParams = { ...providerCfg.auth_params }
      // Social providers may be used to login, or for more detailed actions
      // like posting. Different scopes are required for each
      if (isLogin) {
        authParams.scope = authParams.login_scope
      }
      delete authParams.login_scope

      authParams.state = getMetaString(metaData)
      const authUrl = new URL(providerCfg.auth_url)
      Object.entries(authParams).forEach(([key, val]) => {
        authUrl.searchParams.append(key, encodeURIComponent(val))
      })
      return buildURL(providerCfg.auth_url, authParams)
    },
    async setUserSocialCredentials () {
      const resp = await this.$api.get('user/social-credentials/')
      this.socialCredentials = resp.data
    },
    getUserSocialCredentials () {
      return this.socialCredentials || {}
    }
  }
})
