import { defineStore } from 'pinia'

export const useSlackStore = defineStore('slack', {
  state: () => ({
    slackChannels: {} // employerId: [{slackChannel1}, ...]
  }),

  actions: {
    async setChannels (employerId, isForceRefresh = false) {
      if (!employerId) {
        return
      }
      if (!this.slackChannels[employerId] || isForceRefresh) {
        const resp = await this.$api.get('slack/channel/', {
          params: { employer_id: employerId }
        })
        this.slackChannels[employerId] = resp.data
      }
    },
    getChannels (employerId) {
      return this.slackChannels[employerId]
    }
  }
})
