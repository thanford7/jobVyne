import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userProfiles: {} // {userId: {<userProfile>}
  }),

  actions: {
    async setUserProfile (userId) {
      const resp = await this.$api.get(`user/profile/${userId}/`)
      this.userProfiles[userId] = resp.data
    },
    getUserProfile (userId) {
      return this.userProfiles[userId]
    }
  }
})
