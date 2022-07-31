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
    async setSocialLinkFilters (isForceRefresh = false) {
      if (!isForceRefresh && !dataUtil.isNil(this.socialLinkFilters)) {
        return
      }
      const authStore = useAuthStore()
      const params = {}
      if (authStore.propIsEmployer) {
        params.employer_id = authStore.propUser.employer_id
      } else {
        params.owner_id = authStore.propUser.id
      }

      const resp = await this.$api.get(
        'social-link-filter',
        { params }
      )
      this.socialLinkFilters = resp.data
    },
    getOwnSocialLinkFilters () {
      if (dataUtil.isNil(this.socialLinkFilters)) {
        return []
      }
      const authStore = useAuthStore()
      return this.socialLinkFilters.filter((f) => f.owner_id === authStore.propUser.id)
    },
    getEmployerSocialLinkFilters () {
      return this.socialLinkFilters
    }
  }
})
