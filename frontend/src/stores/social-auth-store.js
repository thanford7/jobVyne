import { defineStore } from 'pinia'
import buildURL from 'axios/lib/helpers/buildURL'

export const useSocialAuthStore = defineStore('social-auth', {
  state: () => ({
    socialCfgs: null
  }),

  actions: {
    async getOauthUrl (provider) {
      if (!this.socialCfgs) {
        const resp = await this.$api.get('social-credentials/')
        this.socialCfgs = resp.data
      }
      const providerCfg = this.socialCfgs[provider]
      return buildURL(providerCfg.auth_url, providerCfg.auth_params)
    }
  }
})
