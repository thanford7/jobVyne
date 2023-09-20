import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    nullValueStr: '[None]',
    nullValueAnyStr: '[Any]',
    websiteName: 'JobVyne',
    currencies: null,
    emailReferral: 'referral@jobvyne.com',
    leverOauthUrl: null
  }),

  actions: {
    async setCurrencies () {
      if (!this.currencies) {
        const resp = await this.$api.get('currency/')
        this.currencies = resp.data
      }
    },
    async setLeverOauthUrl () {
      if (!this.leverOauthUrl) {
        const resp = await this.$api.get('lever/oauth-url/')
        this.leverOauthUrl = resp.data
      }
    },
    getPageTitle (pageName) {
      return `${pageName} - ${this.websiteName}`
    },
    getMetaCfg ({ pageTitle, description = 'Bringing professionals together to help each other get hired, find events, and grow professionally' }) {
      return {
        title: pageTitle,
        titleTemplate: this.getPageTitle,
        // Note these don't currently work because they are dynamically loaded after the page is
        // rendered and social sites scrape the initial page which doesn't have these tags yet.
        // They will work if we eventually switch to SSR
        meta: {
          ogTitle: { property: 'og:title', content: this.getPageTitle(pageTitle) },
          ogDescription: { property: 'og:description', content: description },
          ogUrl: { property: 'og:url', content: window.location.href },
          ogImage: { property: 'og:image', content: process.env.JV_LOGO_URL },
          ogType: { property: 'og:type', content: 'website' },
          ogSiteName: { property: 'og:site_name', content: 'JobVyne' },
          twitterCard: { name: 'twitter:card', content: 'summary_large_image' },
          fbAppId: { property: 'fb:app_id', content: '566736274864908' },
          twitterSite: { name: 'twitter:site', content: '@jobvyne' },
          twitterImgAlt: { name: 'twitter:image:alt', content: 'JobVyne logo' }
        }
      }
    }
  }
})
