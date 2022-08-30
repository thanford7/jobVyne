import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null,
    socialLinkFilters: null
  }),

  actions: {
    async setPlatforms () {
      if (!this.platforms) {
        const resp = await this.$api.get('social-platform/')
        this.platforms = dataUtil.sortBy(resp.data, 'name')
      }
    },
    async setSocialLinkFilters (userId, isForceRefresh = false) {
      if (!isForceRefresh && !dataUtil.isNil(this.socialLinkFilters)) {
        return
      }

      const resp = await this.$api.get(
        'social-link-filter/',
        { params: { owner_id: userId } }
      )
      this.socialLinkFilters = resp.data
    },
    getSocialLinkFilters (userId) {
      if (dataUtil.isNil(this.socialLinkFilters)) {
        return []
      }
      return this.socialLinkFilters.filter((f) => f.owner_id === userId)
    }
  }
})
