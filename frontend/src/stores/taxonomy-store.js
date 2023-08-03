import { defineStore } from 'pinia'

export const useTaxonomyStore = defineStore('taxonomy', {
  state: () => ({
    jobProfessions: null
  }),

  actions: {
    async setJobProfessions (isForceRefresh = false) {
      if (!this.jobProfessions || isForceRefresh) {
        const resp = await this.$api.get('taxonomy/job-profession/')
        this.jobProfessions = resp.data
      }
    },
    getJobProfessions () {
      return this.jobProfessions
    }
  }
})
