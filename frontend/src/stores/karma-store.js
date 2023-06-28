import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data.js'

export const useKarmaStore = defineStore('karma', {
  state: () => ({
    donationOrganizations: null,
    userDonationOrganizations: null,
    userRequests: null,
    userRequest: {}, // {requestId: <userRequestData>, ...}
    userDonations: null
  }),

  actions: {
    async setDonationOrganizations (isForceRefresh = false) {
      if (dataUtil.isNil(this.donationOrganizations) || isForceRefresh) {
        const resp = await this.$api.get('karma/donation-organization/')
        this.donationOrganizations = resp.data
      }
    },
    async setUserDonationOrganizations (userId, isForceRefresh = false) {
      if (dataUtil.isNil(this.userDonationOrganizations) || isForceRefresh) {
        const resp = await this.$api.get('karma/user-donation-organization/', {
          params: { user_id: userId }
        })
        this.userDonationOrganizations = resp.data
      }
    },
    async setUserRequests (userId, isForceRefresh = false) {
      if (dataUtil.isNil(this.userRequests) || isForceRefresh) {
        const resp = await this.$api.get('karma/user-request/', {
          params: { user_id: userId }
        })
        this.userRequests = resp.data
      }
    },
    async setUserRequest (requestId, isForceRefresh = false) {
      if (!this.userRequest[requestId] || isForceRefresh) {
        const resp = await this.$api.get('karma/user-request/', {
          params: { request_id: requestId }
        })
        this.userRequest[requestId] = resp.data
      }
    },
    async setUserDonations (userId, isForceRefresh = false) {
      if (dataUtil.isNil(this.userDonations) || isForceRefresh) {
        const resp = await this.$api.get('karma/user-donation/', {
          params: { user_id: userId }
        })
        this.userDonations = resp.data
      }
    },
    getDonationOrganizations () {
      return this.donationOrganizations || []
    },
    getUserDonationOrganizations () {
      return this.userDonationOrganizations || []
    },
    getUserRequests () {
      return this.userRequests || []
    },
    getUserRequest (requestId) {
      return this.userRequest[requestId]
    },
    getUserDonations () {
      return this.userDonations || []
    }
  }
})
