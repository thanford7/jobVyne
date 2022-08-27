import { defineStore } from 'pinia'

export const useContentStore = defineStore('content', {
  state: () => ({
    socialContent: {},
    userFiles: {} // userId: [<file1>, <file2>, ...]
  }),

  actions: {
    async setSocialContent (employerId, userId, isForceRefresh = false) {
      const key = this.makeSocialContentKey(employerId, userId)
      if (this.socialContent[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('social-content-item/', {
        params: { employer_id: employerId, user_id: userId }
      })
      this.socialContent[key] = resp.data
    },
    async setUserFiles (userId, isForceRefresh = false) {
      if (this.userFiles[userId] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('user/file/', {
        params: { user_id: userId }
      })
      this.userFiles[userId] = resp.data
    },
    getSocialContent (employerId, userId) {
      return this.socialContent[this.makeSocialContentKey(employerId, userId)]
    },
    getUserFiles (userId) {
      return this.userFiles[userId]
    },
    makeSocialContentKey (employerId, userId) {
      return JSON.stringify([employerId, userId])
    }
  }
})
