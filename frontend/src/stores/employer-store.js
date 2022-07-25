import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    employerJobs: {}, // employerId: [<job1>, <job2>, ...]
    employerFiles: {}, // employerId: [<file1>, <file2>, ...],
    employerFileTags: {}, // employerId: [<tag1>, <tag2>, ...]
    permissionGroups: []
  }),

  actions: {
    async setEmployer (employerId, isForceRefresh = false) {
      if (!this.employers[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/${employerId}/`)
        this.employers[employerId] = resp.data
      }
    },
    async setEmployerJobs (employerId, isForceRefresh = false) {
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
    async setEmployerPermissions (isForceRefresh = false) {
      if (!this.permissionGroups.length || isForceRefresh) {
        const resp = await this.$api.get('employer/permission/')
        this.permissionGroups = resp.data
      }
    },
    async setEmployerFiles (employerId, isForceRefresh = false) {
      if (!this.employerFiles[employerId] || isForceRefresh) {
        const resp = await this.$api.get(
          'employer/file/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerFiles[employerId] = resp.data
      }
    },
    async setEmployerFileTags (employerId, isForceRefresh = false) {
      if (!this.employerFileTags[employerId] || isForceRefresh) {
        const resp = await this.$api.get(
          'employer/file-tag/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerFileTags[employerId] = resp.data
      }
    },
    getEmployer (employerId) {
      return this.employers[employerId]
    },
    getEmployerFiles (employerId) {
      return this.employerFiles[employerId]
    },
    getEmployerFileTags (employerId) {
      return dataUtil.sortBy(this.employerFileTags[employerId] || [], 'name')
    },
    getEmployerJobs (employerId) {
      return dataUtil.sortBy(this.employerJobs[employerId] || [], 'job_title')
    },
    getJobDepartments (employerId) {
      if (!this.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        this.employerJobs[employerId].map((j) => ({ department: j.job_department, id: j.job_department_id })),
        'department'
      )
      return dataUtil.sortBy(vals, 'department')
    },
    getJobCities (employerId) {
      if (!this.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        this.employerJobs[employerId].map((j) => ({ city: j.city })),
        'city'
      )
      return dataUtil.sortBy(vals, 'city')
    },
    getJobStates (employerId) {
      if (!this.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        this.employerJobs[employerId].map((j) => ({ state: j.state, id: j.state_id })),
        'state'
      )
      return dataUtil.sortBy(vals, 'state')
    },
    getJobCountries (employerId) {
      if (!this.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        this.employerJobs[employerId].map((j) => ({ country: j.country, id: j.country_id })),
        'country'
      )
      return dataUtil.sortBy(vals, 'country')
    }
  }
})
