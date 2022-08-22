import { defineStore } from 'pinia'
import dateTimeUtil from 'src/utils/datetime.js'

export const useDataStore = defineStore('data', {
  state: () => ({
    socialLinkPerformanceData: {}
  }),

  actions: {
    async getSocialLinkPerformance (startDate, endDate, { employerId, userId }) {
      const apiKey = this.makeApiKey(arguments)
      const data = this.socialLinkPerformanceData[apiKey]
      if (data) {
        return data
      }
      const resp = await this.$api.get('data/link-performance/', {
        params: {
          employer_id: employerId,
          owner_id: userId,
          start_dt: dateTimeUtil.serializeDate(startDate, true),
          end_dt: dateTimeUtil.serializeDate(endDate, true, true)
        }
      })
      this.socialLinkPerformanceData[apiKey] = resp.data
      return resp.data
    },
    makeApiKey (args) {
      return JSON.stringify(args)
    }
  }
})
