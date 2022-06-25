import { defineStore } from 'pinia'
import { getAjaxFormData } from 'src/utils/requests'
import { LocalStorage } from 'quasar'
import dataUtil from 'src/utils/data'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: LocalStorage.getItem('isAuthenticated') || false,
    status: null,
    hasLoadedOnce: false,
    profile: {}
  }),
  getters: {
    authStatus: (state) => state.status,

    getProfile: (state) => state.profile,
    isProfileLoaded: (state) => !dataUtil.isEmpty(state.profile)
  },
  actions: {
    async login (user) {
      this.status = 'loading'
      let resp
      try {
        resp = await this.$api.post('auth/login/', getAjaxFormData(user))
        LocalStorage.set('isAuthenticated', true)
        this.status = 'success'
        this.isAuthenticated = true
        this.hasLoadedOnce = true
      } catch (err) {
        this.status = 'error'
        this.hasLoadedOnce = true
        LocalStorage.remove('isAuthenticated')
        dataUtil.handleAjaxError(err)
        throw err
      }

      try {
        this.profile = await this.$api.get(`user/${resp.data.user_id}/`)
      } catch (err) {
        await this.logout()
        this.status = 'error'
        this.profile = {}
        dataUtil.handleAjaxError(err)
        throw err
      }
    },
    async logout () {
      await this.$api.post('auth/logout/')
      LocalStorage.remove('isAuthenticated')
      this.isAuthenticated = false
    }
  }
})
