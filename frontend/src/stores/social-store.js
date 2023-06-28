import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { getAjaxFormData, makeApiRequestKey } from 'src/utils/requests.js'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null,
    socialLinks: {}, // key: [<socialLink>, ...]
    socialLinkPostJobs: {} // key: [<job1>, ...]
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
    async setSocialLinkPostJobs ({
      userId = null,
      employerId = null,
      socialLinkId = null,
      socialChannel = null,
      isForceRefresh = false
    }) {
      const key = makeApiRequestKey(userId, employerId, socialLinkId, socialChannel)
      if (!isForceRefresh && this.socialLinkPostJobs[key]) {
        return
      }

      const resp = await this.$api.get(
        'social-link-post-jobs/',
        {
          params: {
            user_id: userId,
            employer_id: employerId,
            social_link_id: socialLinkId,
            social_channel: socialChannel
          }
        }
      )
      this.socialLinkPostJobs[key] = resp.data
    },
    async getOrCreateSocialLink (filterData) {
      const resp = await this.$api.post('social-link/', getAjaxFormData(filterData))
      return resp.data.social_link
    },
    getSocialLinks ({ userId = null, employerId = null }) {
      const key = makeApiRequestKey(userId, employerId)
      const socialLinks = this.socialLinks[key]
      return socialLinks || []
    },
    getSocialLinkPostJobs ({ userId = null, employerId = null, socialLinkId = null, socialChannel = null }) {
      const key = makeApiRequestKey(userId, employerId, socialLinkId, socialChannel)
      const socialLinkPostJobs = this.socialLinkPostJobs[key]
      return socialLinkPostJobs || []
    }
  }
})
