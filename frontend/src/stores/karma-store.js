import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data.js'

export const useKarmaStore = defineStore('karma', {
  state: () => ({
    donationOrganizations: null
  }),

  actions: {
    async setDonationOrganizations (isForceRefresh = false) {
      if (dataUtil.isNil(this.donationOrganizations) || isForceRefresh) {
        const resp = await this.$api.get('karma/donation-organization/')
        this.donationOrganizations = resp.data
      }
    },
    getDonationOrganizations () {
      return this.donationOrganizations || []
    }
  }
})
