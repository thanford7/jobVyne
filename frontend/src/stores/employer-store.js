import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    employerJobs: {}, // employerId: [<job1>, <job2>, ...]
    employerBonusRules: {}, // employerId: [<rule1>, <rule2>, ...]
    employerSocialLinks: {}, // employerId: [<link1>, <link2>, ...]
    employerJobLocations: {},
    employerFiles: {}, // employerId: [<file1>, <file2>, ...],
    employerFileTags: {}, // employerId: [<tag1>, <tag2>, ...]
    employerPage: {}, // employerId: {<employerPage>}
    permissionGroups: [],
    employersFromEmail: {} // email: {<employer>}
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
        const jobResp = await this.$api.get(
          'employer/job/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerJobs[employerId] = jobResp.data

        const locResp = await this.$api.get(
          'employer/job/location/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerJobLocations[employerId] = locResp.data
      }
    },
    async setEmployerBonusRules (employerId, isForceRefresh = false) {
      if (!this.employerBonusRules[employerId] || isForceRefresh) {
        const resp = await this.$api.get('employer/bonus/rule/', {
          params: { employer_id: employerId }
        })
        this.employerBonusRules[employerId] = resp.data
      }
    },
    async setEmployerSocialLinks (employerId, isForceRefresh = false) {
      if (!this.employerSocialLinks[employerId] || isForceRefresh) {
        const resp = await this.$api.get('social-link-filter/', {
          params: { employer_id: employerId }
        })
        this.employerSocialLinks[employerId] = resp.data
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
    async setEmployerPage (employerId, isForceRefresh = false) {
      if (!this.employerPage[employerId] || isForceRefresh) {
        const resp = await this.$api.get(
          'employer/page/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerPage[employerId] = resp.data
      }
    },
    async getEmployersFromDomain (email) {
      if (!email) {
        return null
      }
      const employer = this.employersFromEmail[email]
      if (employer) {
        return employer
      }
      const resp = await this.$api.get(
        'employer-from-domain/',
        {
          params: { email }
        }
      )
      this.employersFromEmail[email] = resp.data // Cache the response
      return resp.data
    },
    getEmployer (employerId) {
      return this.employers[employerId]
    },
    getEmployerFiles (employerId, fileId = null) {
      const files = this.employerFiles[employerId]
      if (fileId) {
        if (!files || !files.length) {
          return files
        }
        return files.find((f) => f.id === fileId)
      }
      return files
    },
    getEmployerFileTags (employerId) {
      return dataUtil.sortBy(this.employerFileTags[employerId] || [], 'name')
    },
    getEmployerJobs (employerId) {
      return dataUtil.sortBy(this.employerJobs[employerId] || [], 'job_title')
    },
    getEmployerBonusRules (employerId) {
      return dataUtil.sortBy(this.employerBonusRules[employerId] || [], 'order_idx')
    },
    getEmployerSocialLinks (employerId) {
      return this.employerSocialLinks[employerId] || []
    },
    getEmployerPage (employerId) {
      return this.employerPage[employerId]
    },
    getJobDepartments (employerId) {
      if (!this.employerJobs[employerId]) {
        return null
      }
      const vals = dataUtil.uniqBy(
        this.employerJobs[employerId].map((j) => ({ name: j.job_department, id: j.job_department_id })),
        'name'
      )
      return dataUtil.sortBy(vals, 'name')
    },
    getJobCities (employerId) {
      if (!this.employerJobLocations[employerId]) {
        return null
      }
      return this.employerJobLocations[employerId].cities
    },
    getJobStates (employerId) {
      if (!this.employerJobLocations[employerId]) {
        return null
      }
      return this.employerJobLocations[employerId].states
    },
    getJobCountries (employerId) {
      if (!this.employerJobLocations[employerId]) {
        return null
      }
      return this.employerJobLocations[employerId].countries
    }
  }
})
