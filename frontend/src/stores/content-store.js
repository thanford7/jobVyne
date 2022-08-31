import { defineStore } from 'pinia'

export const useContentStore = defineStore('content', {
  state: () => ({
    socialContent: {},
    userFiles: {}, // userId: [<file1>, <file2>, ...]
    socialPosts: {}
  }),

  actions: {
    async setSocialContent (employerId, userId, isForceRefresh = false) {
      const key = this.makeKey(arguments)
      if (this.socialContent[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('social-content-item/', {
        params: { employer_id: employerId, user_id: userId }
      })
      this.socialContent[key] = resp.data
    },
    async setSocialPosts (employerId, userId, pageNumber, isForceRefresh = false) {
      const key = this.makeKey(arguments)
      if (!isForceRefresh && this.socialPosts[key]) {
        return
      }
      const resp = await this.$api.get(
        'social-post/',
        { params: { user_id: userId, employer_id: employerId, page_count: pageNumber } }
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
      return this.socialContent[this.makeKey(arguments)]
    },
    getSocialPosts (employerId, userId, pageNumber) {
      return this.socialPosts[this.makeKey(arguments)]
    },
    getUserFiles (userId) {
      return this.userFiles[userId]
    },
    makeKey () {
      return JSON.stringify(arguments)
    }
  }
})
