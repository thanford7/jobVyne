import { defineStore } from 'pinia'
import { useAuthStore } from 'stores/auth-store'
import dataUtil from 'src/utils/data'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    employerJobs: {} // employerId: [<job1>, <job2>, ...]
  }),

  getters: {
    getEmployer (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId) {
        return null
      }
      return state.employers[employerId]
    },
    getEmployerJobs (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId) {
        return null
      }
      return dataUtil.sortBy(state.employerJobs[employerId] || [], 'job_title')
    },
    getJobDepartments (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId || !state.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        state.employerJobs[employerId].map((j) => ({ department: j.job_department, id: j.job_department_id })),
        'department'
      )
      return dataUtil.sortBy(vals, 'department')
    },
    getJobCities (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId || !state.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        state.employerJobs[employerId].map((j) => ({ city: j.city })),
        'city'
      )
      return dataUtil.sortBy(vals, 'city')
    },
    getJobStates (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId || !state.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        state.employerJobs[employerId].map((j) => ({ state: j.state, id: j.state_id })),
        'state'
      )
      return dataUtil.sortBy(vals, 'state')
    },
    getJobCountries (state, employerId = null) {
      employerId = employerId || this.getUserEmployerId()
      if (!employerId || !state.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        state.employerJobs[employerId].map((j) => ({ country: j.country, id: j.country_id })),
        'country'
      )
      return dataUtil.sortBy(vals, 'country')
    }
  },

  actions: {
    async setEmployer (employerId = null, isForceRefresh = false) {
      employerId = employerId || this.getUserEmployerId()
      if (!this.employers[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/${employerId}/`)
        this.employers[employerId] = resp.data
      }
    },
    async setEmployerJobs (employerId = null, isForceRefresh = false) {
      employerId = employerId || this.getUserEmployerId()
      if (!this.employerJobs[employerId] || isForceRefresh) {
        const resp = await this.$api.get(
          'employer/job/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerJobs[employerId] = resp.data
      }
    },
    getUserEmployerId () {
      const authStore = useAuthStore()
      return authStore.getProfile.employer_id
    }
  }
})
