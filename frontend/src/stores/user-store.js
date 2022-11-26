import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userProfile: {},
    userEmployeeChecklist: {}
  }),

  actions: {
    async setUserProfile (userId) {
      const resp = await this.$api.get(`user/profile/${userId}/`)
      this.userProfile = resp.data
    },
    async setUserEmployeeChecklist (userId) {
      const resp = await this.$api.get(`user/employee-checklist/${userId}/`)
      this.userEmployeeChecklist = resp.data
    },
    getUserProfile (userId) {
      return this.userProfiles[userId]
    }
  }
})
