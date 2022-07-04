import { defineStore } from 'pinia'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null
  }),

  actions: {
    async setPlatforms () {
      if (!this.platforms) {
        const resp = await this.$api.get('social-platform/')
        this.platforms = resp.data
      }
    }
  }
})
