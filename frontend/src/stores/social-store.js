import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { getAjaxFormData } from 'src/utils/requests.js'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null,
    socialLinkFilters: null
  }),

  actions: {
    async setPlatforms () {
      if (!this.platforms) {
        const resp = await this.$api.get('social-platform/')
        this.platforms = dataUtil.sortBy(resp.data, 'sort_order')
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
    async getOrCreateSocialLinkFilter (filterData) {
      const resp = await this.$api.post('social-link-filter/', getAjaxFormData(filterData))
      return resp.data.link_filter
    },
    getSocialLinkFilters (userId) {
      if (dataUtil.isNil(this.socialLinkFilters)) {
        return []
      }
      return this.socialLinkFilters.filter((f) => f.owner_id === userId)
    }
  }
})
