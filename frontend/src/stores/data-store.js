import { defineStore } from 'pinia'
import dateTimeUtil from 'src/utils/datetime.js'

export const useDataStore = defineStore('data', {
  state: () => ({
    socialLinkPerformanceData: {}
  }),

  actions: {
    async getSocialLinkPerformance (startDate, endDate, { employerId, userId }) {
      startDate = dateTimeUtil.serializeDate(startDate, true)
      endDate = dateTimeUtil.serializeDate(endDate, true, true)
      const apiKey = this.makeApiKey(startDate, endDate, employerId, userId)
      const data = this.socialLinkPerformanceData[apiKey]
      if (data) {
        return data
      }
      const resp = await this.$api.get('data/link-performance/', {
        params: {
          employer_id: employerId,
          owner_id: userId,
          start_dt: startDate,
          end_dt: endDate
        }
      })
      this.socialLinkPerformanceData[apiKey] = resp.data
      return resp.data
    },
    makeApiKey (startDate, endDate, employerId, userId) {
      return JSON.stringify(arguments)
    }
  }
})
