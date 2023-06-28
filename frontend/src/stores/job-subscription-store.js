import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useJobSubscriptionStore = defineStore('jobSubscription', {
  state: () => ({
    jobSubscription: {} // key: [<subscription1>, <subscription2>, ...]
  }),

  actions: {
    async setJobSubscription ({ employerId = null, userId = null, isForceRefresh = false }) {
      const key = makeApiRequestKey(employerId, userId)
      if (!this.jobSubscription[key] || isForceRefresh) {
        const resp = await this.$api.get('job-subscription/', {
          params: { employer_id: employerId, user_id: userId }
        })
        this.jobSubscription[key] = resp.data
      }
    },
    getJobSubscription ({ employerId = null, userId = null }) {
      const key = makeApiRequestKey(employerId, userId)
      return this.jobSubscription[key]
    }
  }
})
