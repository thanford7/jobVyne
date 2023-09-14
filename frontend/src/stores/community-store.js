import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useCommunityStore = defineStore('community', {
  state: () => ({
    members: {}, // {key: [member1, member2, ...]}
    jobConnections: {} // {jobId: [connection1, ...]}
  }),

  actions: {
    async setMembers ({ memberType = null, employerId = null, professionKey = null, isForceRefresh = false }) {
      const key = makeApiRequestKey(memberType, employerId, professionKey)
      if (this.members[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('community/members/', {
        params: { employer_id: employerId, profession_key: professionKey, member_type: memberType }
      })
      this.members[key] = resp.data
    },
    async setJobConnections (
      {
        jobId = null,
        userId = null,
        rowsPerPage = null,
        pageCount = null,
        sortBy = null,
        isDescending = false,
        filters = {},
        groupBy = null,
        isForceRefresh = false
      }
    ) {
      const key = makeApiRequestKey(jobId, userId, rowsPerPage, pageCount, sortBy, isDescending, filters, groupBy)
      if (this.jobConnections[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('community/job-connections/', {
        params: {
          job_id: jobId,
          user_id: userId,
          rows_per_page: rowsPerPage,
          page_count: pageCount,
          sort_order: sortBy,
          is_descending: isDescending,
          filters,
          group_by: groupBy
        }
      })
      this.jobConnections[key] = resp.data
    },
    getMembers ({ memberType = null, employerId = null, professionKey = null }) {
      const key = makeApiRequestKey(memberType, employerId, professionKey)
      return this.members[key] || []
    },
    getJobConnections (
      {
        jobId = null,
        userId = null,
        rowsPerPage = null,
        pageCount = null,
        sortBy = null,
        isDescending = false,
        filters = {},
        groupBy = null
      }
    ) {
      const key = makeApiRequestKey(jobId, userId, rowsPerPage, pageCount, sortBy, isDescending, filters, groupBy)
      return this.jobConnections[key] || []
    }
  }
})
