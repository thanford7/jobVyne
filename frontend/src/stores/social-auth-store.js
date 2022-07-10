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
    socialCfgs: null
  }),

  actions: {
    async getOauthUrl (provider, { redirectPage, redirectParams } = {}) {
      if (!this.socialCfgs) {
        const resp = await this.$api.get('social-credentials/')
        this.socialCfgs = resp.data
      }

      redirectParams = redirectParams || {}
      if (redirectPage) {
        redirectParams.redirectPage = redirectPage
      }

      // redirect_uri is the "fake" url that is intercepted by the router-guard
      // The redirectParams set the page that the user actually ends up on
      // If redirectParams are not provided, the router-guard uses a default redirect page
      const providerCfg = this.socialCfgs[provider]
      providerCfg.auth_params.redirect_uri = buildURL(
        providerCfg.auth_params.redirect_uri,
        redirectParams
      )
      return buildURL(providerCfg.auth_url, providerCfg.auth_params)
    }
  }
})
