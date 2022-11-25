import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    nullValueStr: '[None]',
    nullValueAnyStr: '[Any]',
    websiteName: 'JobVyne',
    currencies: null
  }),

  actions: {
    async setCurrencies () {
      if (!this.currencies) {
        const resp = await this.$api.get('currency/')
        this.currencies = resp.data
      }
    },
    getPageTitle (pageName) {
      return `${pageName} - ${this.websiteName}`
    },
    getMetaCfg ({ pageTitle, description = 'JobVyne helps employees share open positions at their company and get paid for referrals' }) {
      return {
        title: pageTitle,
        titleTemplate: this.getPageTitle,
        meta: {
          ogTitle: { name: 'og:title', content: this.getPageTitle(pageTitle) },
          ogDescription: { name: 'og:description', content: description },
          ogUrl: { name: 'og:url', content: window.location.href },
          ogImage: { name: 'og:image', content: process.env.JV_LOGO_URL },
          ogType: { name: 'og:type', content: 'website' },
          ogSiteName: { name: 'og:site_name', content: 'JobVyne' },
          twitterCard: { name: 'twitter:card', content: 'summary_large_image' },
          fbAppId: { name: 'fb:app_id', content: '566736274864908' },
          twitterSite: { name: 'twitter:site', content: '@jobvyne' },
          twitterImgAlt: { name: 'twitter:image:alt', content: 'JobVyne logo' }
        }
      }
    }
  }
})
