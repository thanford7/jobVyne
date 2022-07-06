import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null
  }),

  actions: {
    async setPlatforms () {
      if (!this.platforms) {
        const resp = await this.$api.get('social-platform/')
        this.platforms = dataUtil.sortBy(resp.data, 'name')
      }
    }
  }
})
