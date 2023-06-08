import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { getAjaxFormData, makeApiRequestKey } from 'src/utils/requests.js'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null,
    socialLinks: {} // key: [<socialLink>, ...]
  }),

  actions: {
    async setPlatforms () {
      if (!this.platforms) {
        const resp = await this.$api.get('social-platform/')
        this.platforms = dataUtil.sortBy(resp.data, 'sort_order')
      }
    },
    async setSocialLinks ({ userId = null, employerId = null, isForceRefresh = false }) {
      const key = makeApiRequestKey(userId, employerId)
      if (!isForceRefresh && this.socialLinks[key]) {
        return
      }

      const resp = await this.$api.get(
        'social-link/',
        { params: { owner_id: userId, employer_id: employerId } }
      )
      this.socialLinks[key] = resp.data
    },
    async getOrCreateSocialLink (filterData) {
      const resp = await this.$api.post('social-link/', getAjaxFormData(filterData))
      return resp.data.link_filter
    },
    getSocialLinks ({ userId = null, employerId = null }) {
      const key = makeApiRequestKey(userId, employerId)
      const socialLinks = this.socialLinks[key]
      return socialLinks || []
    }
  }
})
