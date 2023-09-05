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
    async setJobConnections ({ jobId = null, isForceRefresh = false }) {
      if (this.jobConnections[jobId] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('community/job-connections/', {
        params: { job_id: jobId }
      })
      this.jobConnections[jobId] = resp.data
    },
    getMembers ({ memberType = null, employerId = null, professionKey = null }) {
      const key = makeApiRequestKey(memberType, employerId, professionKey)
      return this.members[key] || []
    },
    getJobConnections (jobId) {
      return this.jobConnections[jobId] || []
    }
  }
})
