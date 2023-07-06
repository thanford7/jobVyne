import { defineStore } from 'pinia'

export const useTaxonomyStore = defineStore('taxonomy', {
  state: () => ({
    jobTitles: null
  }),

  actions: {
    async setJobTitles (isForceRefresh = false) {
      if (!this.jobTitles || isForceRefresh) {
        const resp = await this.$api.get('taxonomy/job-title/')
        this.jobTitles = resp.data
      }
    },
    getJobTitles () {
      return this.jobTitles
    }
  }
})
