import { defineStore } from 'pinia'
import buildURL from 'axios/lib/helpers/buildURL'

/*
This is the process for social authentication:
(1) User clicks button to use a social platform for authentication
(2) User is sent to the social platform's auth page
(3) User is redirected to a "fake" JobVyne auth page which is caught in router-guards
(4) The router-guard uses the credentials from the incoming url to authenticate the user
(5) The router-guard redirects the user to the ultimate page they land on
 */

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
      providerCfg.auth_params.state = JSON.stringify({
        state: providerCfg.auth_params.state,
        redirectPageUrl,
        redirectParams,
        userTypeBit,
        isLogin
      })
      return buildURL(providerCfg.auth_url, providerCfg.auth_params)
    },
    async setUserSocialCredentials (isForceRefresh) {
      if (!isForceRefresh && this.socialCredentials) {
        return
      }
      const resp = await this.$api.get('user/social-credentials/')
      this.socialCredentials = resp.data
    }
  }
})
