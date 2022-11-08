import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

export const useDataStore = defineStore('data', {
  state: () => ({
    applications: [],
    pageViews: [],
    socialLinkPerformanceData: {}
  }),

  actions: {
    async getData (url, dataAttr, startDate, endDate, extraParams = {}) {
      startDate = dateTimeUtil.serializeDate(startDate, true)
      endDate = dateTimeUtil.serializeDate(endDate, true, true)
      const apiKey = this.makeApiKey(startDate, endDate, extraParams)
      const data = this[dataAttr][apiKey]
      if (data) {
        return data
      }
      const resp = await this.$api.get(url, {
        params: Object.assign({
          start_dt: startDate,
          end_dt: endDate
        }, extraParams)
      })
      this[dataAttr][apiKey] = resp.data
      return dataUtil.deepCopy(resp.data) // Copy to avoid mutation
    },
    async getApplications (startDate, endDate, params) {
      return await this.getData(
        'data/applications/',
        'applications',
        startDate, endDate, params
      )
    },
    async getPageViews (startDate, endDate, params) {
      return await this.getData(
        'data/page-views/',
        'pageViews',
        startDate, endDate, params
      )
    },
    makeApiKey (startDate, endDate, extraParams) {
      return JSON.stringify(arguments)
    }
  }
})
