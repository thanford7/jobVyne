import { defineStore } from 'pinia'
import { getAjaxFormData } from 'src/utils/requests'
import { useAuthStore } from 'stores/auth-store'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    employerJobs: {} // employerId: [<job1>, <job2>, ...]
  }),

  getters: {
    getEmployer (employerId) {
      return this.employers[employerId]
    }
  },

  actions: {
    async setEmployer (employerId = null, isForceRefresh = false) {
      employerId = employerId || this.getUserEmployerId()
      if (!this.employers[employerId] || isForceRefresh) {
        this.employers[employerId] = await this.$api.get(`employer/${employerId}/`)
      }
    },
    async setEmployerJobs (employerId = null, isForceRefresh = false) {
      employerId = employerId || this.getUserEmployerId()
      if (!this.employerJobs[employerId] || isForceRefresh) {
        this.employerJobs[employerId] = await this.$api.get(
          'employer/job/',
          {
            params: { employer_id: employerId }
          }
        )
      }
    },
    getUserEmployerId () {
      const authStore = useAuthStore()
      return authStore?.profile?.employer_id
    }
  }
})
