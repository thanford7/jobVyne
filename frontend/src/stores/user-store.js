import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userProfile: {}, // key: {profile}
    userEmployeeChecklist: {}
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
    getUserProfile ({ userId = null, socialLinkId = null }) {
      return this.userProfile[userId || socialLinkId]
    }
  }
})
