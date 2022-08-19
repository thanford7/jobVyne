import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

export const useDataStore = defineStore('data', {
  state: () => ({
    socialLinkPerformanceData: {}
  }),

  actions: {
    async setSocialLinkPerformance (employerId, startDate, endDate) {
      startDate = dateTimeUtil.serializeDate(startDate)
      endDate = dateTimeUtil.serializeDate(endDate)
      const apiKey = this.makeApiKey(arguments)
      const data = this.socialLinkPerformanceData[apiKey]
      if (data) {
        return
      }
      const resp = await this.$api.get('data/link-performance/', {
        params: {
          employer_id: employerId,
          start_date: startDate,
          end_date: endDate
        }
      })
      this.socialLinkPerformanceData[apiKey] = resp.data
    },
    getSocialLinkPerformance (employerId, startDate, endDate) {
      startDate = dateTimeUtil.serializeDate(startDate)
      endDate = dateTimeUtil.serializeDate(endDate)
      const apiKey = this.makeApiKey(arguments)
      return dataUtil.deepCopy(this.socialLinkPerformanceData[apiKey])
    },
    makeApiKey (args) {
      return JSON.stringify(args)
    }
  }
})
