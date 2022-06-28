import { defineStore } from 'pinia'
import { getAjaxFormData } from 'src/utils/requests'
import { LocalStorage } from 'quasar'
import dataUtil from 'src/utils/data'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: LocalStorage.getItem('isAuthenticated') || false,
    profile: LocalStorage.getItem('profile') || {}
  }),
  getters: {
    getProfile: (state) => state.profile,
    isProfileLoaded: (state) => !dataUtil.isEmpty(state.profile)
  },
  actions: {
    async login (user) {
      // TODO: Add loading indicator
      let resp
      try {
        resp = await this.$api.post('auth/login/', getAjaxFormData(user))
        this.updateStatus(true)
      } catch (err) {
        this.updateStatus(false)
        dataUtil.handleAjaxError(err)
        throw err
      }
      await this.setUserProfile(resp.data.user_id)
    },
    async logout () {
      await this.$api.post('auth/logout/')
      this.updateStatus(false)
      this.profile = {}
    },
    async setUserProfile (userId) {
      try {
        const userResp = await this.$api.get(`user/${userId}/`)
        this.profile = userResp.data
        LocalStorage.set('profile', userResp.data)
      } catch (err) {
        dataUtil.handleAjaxError(err)
        throw err
      }
    },
    updateStatus (isLoggedIn) {
      if (isLoggedIn) {
        LocalStorage.set('isAuthenticated', true)
        this.isAuthenticated = true
      } else {
        LocalStorage.remove('isAuthenticated')
        LocalStorage.remove('profile')
        this.isAuthenticated = false
      }
    }
  }
})
