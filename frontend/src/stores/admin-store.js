import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    employers: {},
    jobScrapers: [],
    paginatedUsers: {}, // {total_page_count: <int>, total_user_count: <int>, users: [<user1>, ...]}
    failedAtsApplications: [],
    processedJobsData: {}
  }),

  actions: {
    async setPaginatedEmployers ({ pageCount = 1, filterBy = null, isForce = false }) {
      const key = makeApiRequestKey(pageCount, filterBy)
      if (!isForce && this.employers[key]) {
        return
      }
      const resp = await this.$api.get('admin/employer/', {
        params: { page_count: pageCount, filter_by: filterBy }
      })
      this.employers[key] = resp.data
    },
    async setJobScrapers (isForce = false) {
      if (!this.jobScrapers.length || isForce) {
        const resp = await this.$api.get('admin/job-scraper/')
        this.jobScrapers = resp.data
      }
    },
    async setUsers (pageCount, sortOrder, isDescending = false, filters = {}) {
      const resp = await this.$api.get('admin/user/', {
        params: { page_count: pageCount, filters, sort_order: sortOrder, is_descending: isDescending }
      })
      this.paginatedUsers = resp.data
    },
    async setFailedAtsApplications (isForce = false) {
      if (!this.failedAtsApplications.length || isForce) {
        const resp = await this.$api.get('admin/ats-failure/')
        this.failedAtsApplications = resp.data
      }
    },
    async setProcessedJobsData () {
      const resp = await this.$api.get('data/admin/processed-jobs/')
      this.processedJobsData = resp.data
    },
    getPaginatedEmployers ({ pageCount = 1, filterBy = null }) {
      const key = makeApiRequestKey(pageCount, filterBy)
      return this.employers[key] || {}
    }
  }
})
