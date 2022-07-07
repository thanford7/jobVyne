import { defineStore } from 'pinia'
import { useAuthStore } from 'stores/auth-store'
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
    async setSocialLinkFilters () {
      const authStore = useAuthStore()
      const params = {}
      if (authStore.getIsEmployer) {
        params.employer_id = authStore.getProfile.employer_id
      } else {
        params.owner_id = authStore.getProfile.id
      }

      const resp = await this.$api.get(
        'social-link-filter',
        { params }
      )
      this.socialLinkFilters = resp.data
    }
  }
})
