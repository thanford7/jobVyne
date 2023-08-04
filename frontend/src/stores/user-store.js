import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    userProfile: {}, // key: {profile}
    userEmployeeChecklist: {},
    userCreatedJobs: {} // key: pagedUserData
  }),

  actions: {
    async setUserProfile ({ userId = null, socialLinkId = null, isForceRefresh = false }) {
      if (!userId && !socialLinkId) {
        return
      }
      if (!isForceRefresh && this.userProfile[userId || socialLinkId]) {
        return
      }
      const resp = await this.$api.get('user/profile/', {
        params: {
          user_id: userId,
          social_link_id: socialLinkId
        }
      })
      this.userProfile[userId || socialLinkId] = resp.data
    },
    async setUserEmployeeChecklist (userId) {
      const resp = await this.$api.get(`user/employee-checklist/${userId}/`)
      this.userEmployeeChecklist = resp.data
    },
    async setPaginatedUserCreatedJobs ({ pageCount = 1, userId = null, isApproved = null, isClosed = false, isForceRefresh = false }) {
      const key = makeApiRequestKey(pageCount, userId, isApproved, isClosed)
      if (this.userCreatedJobs[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('user/created-jobs/', {
        params: {
          page_count: pageCount,
          user_id: userId,
          is_approved: isApproved
        }
      })
      this.userCreatedJobs[key] = resp.data
    },
    getUserProfile ({ userId = null, socialLinkId = null }) {
      return this.userProfile[userId || socialLinkId]
    },
    getPaginatedUserCreatedJobs ({ pageCount = 1, userId = null, isApproved = null, isClosed = false }) {
      const key = makeApiRequestKey(pageCount, userId, isApproved, isClosed)
      return this.userCreatedJobs[key] || []
    }
  }
})
