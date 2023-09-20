import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    allEmployers: [],
    employees: {}, // employerId: [<employee1>, <employee2>, ...]
    employerBilling: {}, // employerId: <billingData>
    employerJobs: {}, // employerId: [<job1>, <job2>, ...]
    employerJobApplicationRequirements: {},
    employerJobDepartments: {}, // employerId: [<jobDept1>, <jobDept2>, ...]
    employerReferralRequests: {}, // employerId: [<request1>, <request2>, ...]
    employerBonusRules: {}, // employerId: [<rule1>, <rule2>, ...]
    employerSubscription: {}, // employerId: {subscription data}
    employerJobLocations: {},
    employerFiles: {}, // employerId: [<file1>, <file2>, ...],
    employerFileTags: {}, // employerId: [<tag1>, <tag2>, ...]
    permissionGroups: {}, // employerId: [<group1>, ...]
    employersFromEmail: {} // email: {<employer>}
  }),

  actions: {
    async setEmployer (employerId, isForceRefresh = false) {
      if (!employerId) {
        return
      }
      if (!this.employers[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/${employerId}/`)
        this.employers[employerId] = resp.data
      }
    },
    async setAllEmployers (isForceRefresh = false) {
      if (!this.allEmployers.length || isForceRefresh) {
        const resp = await this.$api.get('employer/')
        this.allEmployers = resp.data
      }
    },
    async setEmployees (employerId, isForceRefresh = false) {
      if (!this.employees[employerId] || isForceRefresh) {
        const resp = await this.$api.get('user/', {
          params: { employer_id: employerId }
        })
        this.employees[employerId] = resp.data
      }
    },
    async setEmployerBilling (employerId, isForceRefresh = false) {
      if (!this.employerBilling[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/billing/${employerId}/`)
        this.employerBilling[employerId] = resp.data
      }
    },
    async setEmployerJobs (employerId, { isOnlyClosed = false, isIncludeClosed = false, isForceRefresh = false } = {}) {
      const apiRequestKey = makeApiRequestKey(employerId, isOnlyClosed, isIncludeClosed)
      if (!this.employerJobs[apiRequestKey] || isForceRefresh) {
        const jobResp = await this.$api.get(
          'employer/job/',
          {
            params: { employer_id: employerId, is_only_closed: isOnlyClosed, is_include_closed: isIncludeClosed }
          }
        )
        this.employerJobs[apiRequestKey] = jobResp.data

        const locResp = await this.$api.get(
          'employer/job/location/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerJobLocations[employerId] = locResp.data
      }
    },
    async setEmployerJobApplicationRequirements ({ employerId = null, jobId = null, isForceRefresh = false }) {
      if (!(employerId || jobId)) {
        return
      }
      const apiRequestKey = makeApiRequestKey(employerId, jobId)
      if (this.employerJobApplicationRequirements[apiRequestKey] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get(
        'employer/job-application-requirement/',
        {
          params: { employer_id: employerId, job_id: jobId }
        }
      )
      this.employerJobApplicationRequirements[apiRequestKey] = resp.data
    },
    async setEmployerJobDepartments (employerId, isForceRefresh = false) {
      if (!this.employerJobDepartments[employerId] || isForceRefresh) {
        const resp = await this.$api.get(
          'employer/job/department/',
          {
            params: { employer_id: employerId }
          }
        )
        this.employerJobDepartments[employerId] = resp.data
      }
    },
    async setEmployerReferralRequests (employerId, isForceRefresh = false) {
      if (!this.employerReferralRequests[employerId] || isForceRefresh) {
        const resp = await this.$api.get('employer/referral/request/', {
          params: { employer_id: employerId }
        })
        this.employerReferralRequests[employerId] = resp.data
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
    async setEmployerSubscription (employerId, isForceRefresh = false) {
      if (!this.employerSubscription[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/subscription/${employerId}/`)
        this.employerSubscription[employerId] = resp.data
      }
    },
    async setEmployerPermissions (employerId, isForceRefresh = false) {
      if (!this.permissionGroups[employerId] || isForceRefresh) {
        const resp = await this.$api.get('employer/permission/', {
          params: {
            employer_id: employerId
          }
        })
        this.permissionGroups[employerId] = resp.data
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
    async setEmployersFromDomain (email, isForceRefresh = false) {
      if (!email) {
        return
      }
      if (this.employersFromEmail[email] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get(
        'employer-from-domain/',
        {
          params: { email }
        }
      )
      this.employersFromEmail[email] = resp.data
    },
    getEmployersFromDomain (email) {
      return this.employersFromEmail[email]
    },
    getEmployer (employerId) {
      return this.employers[employerId]
    },
    getEmployees (employerId) {
      return this.employees[employerId]
    },
    getEmployerBilling (employerId) {
      return this.employerBilling[employerId]
    },
    getEmployerPermissions (employerId) {
      return this.permissionGroups[employerId]
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
    getEmployerJobs (employerId, { isOnlyClosed = false, isIncludeClosed = false } = {}) {
      const apiRequestKey = makeApiRequestKey(employerId, isOnlyClosed, isIncludeClosed)
      return dataUtil.sortBy(this.employerJobs[apiRequestKey] || [], 'job_title')
    },
    getEmployerJobApplicationRequirements ({ employerId = null, jobId = null }) {
      const apiRequestKey = makeApiRequestKey(employerId, jobId)
      return this.employerJobApplicationRequirements[apiRequestKey]
    },
    getEmployerReferralRequests (employerId) {
      return dataUtil.sortBy(this.employerReferralRequests[employerId] || [], { key: 'modified_dt', direction: -1 })
    },
    getEmployerBonusRules (employerId) {
      return dataUtil.sortBy(this.employerBonusRules[employerId] || [], 'order_idx')
    },
    getEmployerSubscription (employerId) {
      return this.employerSubscription[employerId]
    },
    getEmployerJobDepartments (employerId) {
      const departments = this.employerJobDepartments[employerId]
      return dataUtil.sortBy(departments || [], 'name')
    },
    getJobLocations (employerId) {
      if (!this.employerJobLocations[employerId]) {
        return null
      }
      return this.employerJobLocations[employerId].locations
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
