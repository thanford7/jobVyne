import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data.js'

export const useBillingStore = defineStore('billing', {
  state: () => ({
    isLive: null,
    products: [],
    employerCharges: {},
    employerInvoices: {},
    employerSubscription: {}, // employerId: <subscription>
    employerPaymentSetup: {}, // employerId: <setup secret key>
    employerPaymentMethods: {} // employerId: [<method1>, <method2>, ...]
  }),

  actions: {
    async setProducts () {
      const resp = await this.$api.get('billing/product/')
      this.products = resp.data
    },
    async setEmployerCharges (employerId, isForceRefresh = false) {
      if (!this.employerCharges[employerId] || isForceRefresh) {
        const resp = await this.$api.get('billing/charge/', {
          params: { employer_id: employerId }
        })
        this.employerCharges[employerId] = resp.data
      }
    },
    async setEmployerInvoices (employerId, isForceRefresh = false) {
      if (!this.employerInvoices[employerId] || isForceRefresh) {
        const resp = await this.$api.get('billing/invoice/', {
          params: { employer_id: employerId }
        })
        this.employerInvoices[employerId] = resp.data
      }
    },
    async setEmployerSubscription (employerId, isForceRefresh = false) {
      if (!this.employerSubscription[employerId] || isForceRefresh) {
        const resp = await this.$api.get('billing/subscription/', {
          params: { employer_id: employerId }
        })
        this.employerSubscription[employerId] = resp.data
      }
    },
    async setEmployerPaymentSetup (employerId, isForceRefresh = false) {
      if (!this.employerPaymentSetup[employerId] || isForceRefresh) {
        const resp = await this.$api.get('billing/setup/', {
          params: { employer_id: employerId }
        })
        const { client_secret: setupSecretKey } = resp.data
        this.employerPaymentSetup[employerId] = setupSecretKey
      }
    },
    async setEmployerPaymentMethods (employerId, isForceRefresh = false) {
      if (!this.employerPaymentMethods[employerId] || isForceRefresh) {
        const resp = await this.$api.get('billing/payment-method/', {
          params: { employer_id: employerId }
        })
        this.employerPaymentMethods[employerId] = resp.data
      }
    },
    async setIsPaymentLive () {
      if (dataUtil.isNil(this.isLive)) {
        const resp = await this.$api.get('billing/test-status/')
        this.isLive = resp.data.is_live
      }
    },
    getProducts () {
      return this.products
    },
    getEmployerCharges (employerId) {
      return this.employerCharges[employerId]
    },
    getEmployerInvoices (employerId) {
      return this.employerInvoices[employerId]
    },
    getEmployerSubscription (employerId) {
      return this.employerSubscription[employerId]
    },
    getEmployerPaymentSetup (employerId) {
      return this.employerPaymentSetup[employerId]
    },
    getEmployerPaymentMethods (employerId) {
      return this.employerPaymentMethods[employerId]
    }
  }
})
