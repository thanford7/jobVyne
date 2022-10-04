import { defineStore } from 'pinia'

export const useBillingStore = defineStore('billing', {
  state: () => ({
    products: [],
    employerSubscription: {}, // employerId: <subscription>
    employerPaymentSetup: {}, // employerId: <setup secret key>
    employerPaymentMethods: {} // employerId: [<method1>, <method2>, ...]
  }),

  actions: {
    async setProducts () {
      const resp = await this.$api.get('billing/product/')
      this.products = resp.data
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
    getProducts () {
      return this.products
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
