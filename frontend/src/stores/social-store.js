import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { getAjaxFormData, makeApiRequestKey } from 'src/utils/requests.js'

export const useSocialStore = defineStore('social', {
  state: () => ({
    platforms: null,
    socialLinks: {}, // key: [<socialLink>, ...]
    socialLinkJobs: {}, // key: {}
    socialLinkPostJobs: {}, // key: [<job1>, ...]
    socialLinkEmployer: {} // key: {}
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
    async setSocialLinkJobs ({
      linkId = null,
      employerKey = null,
      isEmployer = null,
      professionKey = null,
      jobSubscriptionIds = null,
      pageNumber = 1,
      jobFilters = null,
      isForceRefresh = false
    }) {
      const key = makeApiRequestKey(linkId, employerKey, isEmployer, professionKey, jobSubscriptionIds, pageNumber, JSON.stringify(jobFilters))
      if (!isForceRefresh && this.socialLinkJobs[key]) {
        return
      }

      const resp = await this.$api.get('social-link-jobs/', {
        params: {
          link_id: linkId,
          employer_key: employerKey,
          is_employer: isEmployer,
          profession_key: professionKey,
          job_subscription_ids: jobSubscriptionIds,
          page_count: pageNumber,
          job_filters: jobFilters
        }
      })
      this.socialLinkJobs[key] = resp.data
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
    async setSocialLinkEmployer ({ socialLinkId = null, employerKey = null, isForceRefresh = false }) {
      if (!socialLinkId && !employerKey) {
        return
      }
      const key = makeApiRequestKey(socialLinkId, employerKey)
      if (!isForceRefresh && this.socialLinkEmployer[key]) {
        return
      }
      const resp = await this.$api.get('employer/', {
        params: {
          social_link_id: socialLinkId,
          employer_key: employerKey
        }
      })
      this.socialLinkEmployer[key] = resp.data
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
    getSocialLinkJobs ({
      linkId = null,
      employerKey = null,
      isEmployer = null,
      professionKey = null,
      jobSubscriptionIds = null,
      pageNumber = 1,
      jobFilters = null
    }) {
      const key = makeApiRequestKey(linkId, employerKey, isEmployer, professionKey, jobSubscriptionIds, pageNumber, JSON.stringify(jobFilters))
      return this.socialLinkJobs[key]
    },
    getSocialLinkPostJobs ({ userId = null, employerId = null, socialLinkId = null, socialChannel = null }) {
      const key = makeApiRequestKey(userId, employerId, socialLinkId, socialChannel)
      const socialLinkPostJobs = this.socialLinkPostJobs[key]
      return socialLinkPostJobs || []
    },
    getSocialLinkEmployer ({ socialLinkId = null, employerKey = null }) {
      const key = makeApiRequestKey(socialLinkId, employerKey)
      return this.socialLinkEmployer[key]
    }
  }
})
