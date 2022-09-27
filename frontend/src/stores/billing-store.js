import { defineStore } from 'pinia'

export const useBillingStore = defineStore('billing', {
  state: () => ({
    products: []
  }),

  actions: {
    async setProducts () {
      const resp = await this.$api.get('billing/product/')
      this.products = resp.data
    },
    getProducts () {
      return this.products
    }
  }
})
