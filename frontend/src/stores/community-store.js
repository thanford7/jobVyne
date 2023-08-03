import { defineStore } from 'pinia'
import { makeApiRequestKey } from 'src/utils/requests.js'

export const useCommunityStore = defineStore('community', {
  state: () => ({
    members: {} // {key: [member1, member2, ...]}
  }),

  actions: {
    async setMembers (memberType, { employerId = null, professionKey = null, isForceRefresh = false }) {
      const key = makeApiRequestKey(memberType, employerId, professionKey)
      if (this.members[key] && !isForceRefresh) {
        return
      }
      const resp = await this.$api.get('community/members/', {
        params: { employer_id: employerId, profession_key: professionKey, member_type: memberType }
      })
      this.members[key] = resp.data
    },
    getMembers (memberType, { employerId = null, professionKey = null }) {
      const key = makeApiRequestKey(memberType, employerId, professionKey)
      return this.members[key] || []
    }
  }
})
