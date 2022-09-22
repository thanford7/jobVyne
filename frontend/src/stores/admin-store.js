import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    employers: []
  }),

  actions: {
    async setEmployers (isForce = false) {
      if (!this.employers.length || isForce) {
        const resp = await this.$api.get('admin/employer/')
        this.employers = resp.data
      }
    }
  }
})
