import { defineStore } from 'pinia'

export const useTaxonomyStore = defineStore('taxonomy', {
  state: () => ({
    jobProfessions: null,
    jobLevels: null
  }),

  actions: {
    async setJobProfessions (isForceRefresh = false) {
      if (!this.jobProfessions || isForceRefresh) {
        const resp = await this.$api.get('taxonomy/job-profession/')
        this.jobProfessions = resp.data
      }
    },
    async setJobLevels (isForceRefresh = false) {
      if (!this.jobLevels || isForceRefresh) {
        const resp = await this.$api.get('taxonomy/job-level/')
        this.jobLevels = resp.data
      }
    },
    getJobProfessions () {
      return this.jobProfessions
    },
    getJobLevels () {
      return this.jobLevels
    }
  }
})
