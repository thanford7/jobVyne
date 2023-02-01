import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    employers: [],
    jobScrapers: [],
    paginatedUsers: {}, // {total_page_count: <int>, total_user_count: <int>, users: [<user1>, ...]}
    failedAtsApplications: []
  }),

  actions: {
    async setEmployers (isForce = false) {
      if (!this.employers.length || isForce) {
        const resp = await this.$api.get('admin/employer/')
        this.employers = resp.data
      }
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
    }
  }
})
