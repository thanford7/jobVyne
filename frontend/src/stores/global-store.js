import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    nullValueStr: '[None]',
    nullValueAnyStr: '[Any]',
    websiteName: 'JobVyne'
  }),

  actions: {
    getPageTitle (pageName) {
      return `${pageName} - ${this.websiteName}`
    }
  }
})
