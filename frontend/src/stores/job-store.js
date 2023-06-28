import { defineStore } from 'pinia'

export const useJobStore = defineStore('job', {
  state: () => ({
    jobDepartments: [],
    locations: {}
  }),

  actions: {
    async setJobDepartments () {
      const resp = await this.$api.get('job/department/')
      this.jobDepartments = resp.data
    },
    async setLocations () {
      const resp = await this.$api.get('job/location/')
      this.locations = resp.data
    },
    getJobDepartments () {
      return this.jobDepartments
    },
    getLocations () {
      return this.locations.locations
    },
    getCities () {
      return this.locations.cities
    },
    getStates () {
      return this.locations.states
    },
    getCountries () {
      return this.locations.countries
    }
  }
})
