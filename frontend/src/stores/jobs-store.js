import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useJobsStore = defineStore('jobs', {
  state: () => ({
    paginatedJobs: {} // requestKey: {}
  }),

  actions: {
    async setJobs (pagination, { isForceRefresh = false, filterParams = {} } = {}) {
      const key = makeApiRequestKey(pagination, filterParams)
      if (!this.paginatedJobs[key] || isForceRefresh) {
        const resp = await this.$api.get('jobs/', {
          params: { pagination, filterParams }
        })
        this.paginatedJobs[key] = resp.data
      }
    },
    getJobs (pagination, filterParams) {
      const key = makeApiRequestKey(pagination, filterParams)
      return this.paginatedJobs[key]
    }
  }
})
