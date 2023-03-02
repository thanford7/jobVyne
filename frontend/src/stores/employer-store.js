import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

export const useEmployerStore = defineStore('employer', {
  state: () => ({
    employers: {}, // employerId: {<employer>}
    allEmployers: [],
    employees: {}, // employerId: [<employee1>, <employee2>, ...]
    employerBilling: {}, // employerId: <billingData>
    employerJobs: {}, // employerId: [<job1>, <job2>, ...]
    employerJobDepartments: {}, // employerId: [<jobDept1>, <jobDept2>, ...]
    employerReferralRequests: {}, // employerId: [<request1>, <request2>, ...]
    employerBonusRules: {}, // employerId: [<rule1>, <rule2>, ...]
    employerSocialLinks: {}, // employerId: [<link1>, <link2>, ...]
    employerSubscription: {}, // employerId: {subscription data}
    employerJobSubscription: {}, // employerId: [<subscription1>, <subscription2>, ...]
    employerJobLocations: {},
    employerFiles: {}, // employerId: [<file1>, <file2>, ...],
    employerFileTags: {}, // employerId: [<tag1>, <tag2>, ...]
    employerPage: {}, // employerId: {<employerPage>}
    permissionGroups: [],
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
    async setEmployerSocialLinks (employerId, isForceRefresh = false) {
      if (!this.employerSocialLinks[employerId] || isForceRefresh) {
        const resp = await this.$api.get('social-link-filter/', {
          params: { employer_id: employerId }
        })
        this.employerSocialLinks[employerId] = resp.data
      }
    },
    async setEmployerSubscription (employerId, isForceRefresh = false) {
      if (!this.employerSubscription[employerId] || isForceRefresh) {
        const resp = await this.$api.get(`employer/subscription/${employerId}/`)
        this.employerSubscription[employerId] = resp.data
      }
    },
    async setEmployerJobSubscription (employerId, isForceRefresh = false) {
      if (!this.employerJobSubscription[employerId] || isForceRefresh) {
        const resp = await this.$api.get('employer/job-subscription/', {
          params: { employer_id: employerId }
        })
        this.employerJobSubscription[employerId] = resp.data
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
    getEmployerReferralRequests (employerId) {
      return dataUtil.sortBy(this.employerReferralRequests[employerId] || [], { key: 'modified_dt', direction: -1 })
    },
    getEmployerBonusRules (employerId) {
      return dataUtil.sortBy(this.employerBonusRules[employerId] || [], 'order_idx')
    },
    getEmployerSocialLinks (employerId) {
      return this.employerSocialLinks[employerId] || []
    },
    getEmployerSubscription (employerId) {
      return this.employerSubscription[employerId]
    },
    getEmployerJobSubscription (employerId) {
      return this.employerJobSubscription[employerId]
    },
    getEmployerPage (employerId) {
      return this.employerPage[employerId]
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
