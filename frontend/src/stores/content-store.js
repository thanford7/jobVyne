import { defineStore } from 'pinia'

export const useContentStore = defineStore('content', {
  state: () => ({
    socialContent: {},
    userFiles: {}, // userId: [<file1>, <file2>, ...]
    socialPosts: {}
  }),

  actions: {
    async setSocialContent (employerId, userId, isForceRefresh = false) {
      const key = this.makeKey(employerId, userId)
      if (this.socialContent[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('social-content-item/', {
        params: { employer_id: employerId, user_id: userId }
      })
      this.socialContent[key] = resp.data
    },
    async setSocialPosts (employerId, userId, isForceRefresh = false) {
      const key = this.makeKey(employerId, userId)
      if (!isForceRefresh && this.socialPosts[key]) {
        return
      }
      const resp = await this.$api.get(
        'social-post',
        { params: { user_id: userId, employer_id: employerId } }
      )
      this.socialPosts[key] = resp.data
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
      return this.socialContent[this.makeKey(employerId, userId)]
    },
    getSocialPosts (employerId, userId) {
      return this.socialPosts[this.makeKey(employerId, userId)]
    },
    getUserFiles (userId) {
      return this.userFiles[userId]
    },
    makeKey (employerId, userId) {
      return JSON.stringify([employerId, userId])
    }
  }
})
