import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    userNotificationPreferences: {} // userId: [<preference1>, ...]
  }),

  actions: {
    async setUserNotificationPreferences (userId, isForceRefresh = false) {
      if (!this.userNotificationPreferences[userId] || isForceRefresh) {
        const resp = await this.$api.get('notification-preference/', {
          params: { user_id: userId }
        })
        this.userNotificationPreferences[userId] = resp.data
      }
    },
    getUserNotificationPreferences (userId) {
      return this.userNotificationPreferences[userId]
    }
  }
})
