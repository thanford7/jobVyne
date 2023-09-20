import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    userProfile: {}, // key: {profile}
    userEmployeeChecklist: {},
    userCreatedJobs: {}, // key: pagedUserData
    userFavorites: {} // key: {favorites}
  }),

  actions: {
    async setUserProfile ({ userId = null, userKey = null, isForceRefresh = false }) {
      if (!userId && !userKey) {
        return
      }
      if (!isForceRefresh && this.userProfile[userId || userKey]) {
        return
      }
      const resp = await this.$api.get('user/profile/', {
        params: {
          user_id: userId,
          user_key: userKey
        }
      })
      this.userProfile[userId || userKey] = resp.data
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
          is_approved: isApproved,
          is_closed: isClosed
        }
      })
      this.userCreatedJobs[key] = resp.data
    },
    async setUserFavorites (userId, { isForceRefresh = false } = {}) {
      if (this.userFavorites[userId] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('user/favorite/', {
        params: { user_id: userId }
      })
      this.userFavorites[userId] = resp.data
    },
    getUserProfile ({ userId = null, userKey = null }) {
      return this.userProfile[userId || userKey]
    },
    getPaginatedUserCreatedJobs ({ pageCount = 1, userId = null, isApproved = null, isClosed = false }) {
      const key = makeApiRequestKey(pageCount, userId, isApproved, isClosed)
      return this.userCreatedJobs[key] || []
    },
    getUserFavorites (userId) {
      return this.userFavorites[userId]
    }
  }
})
