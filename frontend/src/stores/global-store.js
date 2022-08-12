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
    }
  }
})
