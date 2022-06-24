import { defineStore } from 'pinia'
import { Cookies, LocalStorage } from 'quasar'
import dataUtil from 'src/utils/data'
import globalData from 'src/utils/global'
import axios from 'axios'

const csrftoken = Cookies.get('csrftoken')
const api = axios.create({
  baseURL: process.env.API,
  headers: { 'X-CSRFTOKEN': csrftoken }
})

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: LocalStorage.getItem('isAuthenticated') || false,
    status: null,
    hasLoadedOnce: false,
    profile: {}
  }),
  getters: {
    getAuthenticated: (state) => state.isAuthenticated,
    isAuthenticated: (state) => state.isAuthenticated,
    authStatus: (state) => state.status,

    getProfile: (state) => state.profile,
    isProfileLoaded: (state) => !dataUtil.isEmpty(state.profile)
  },
  actions: {
    login: (user) => {
      return new Promise((resolve, reject) => {
        this.status = 'loading'
        api
          .post('/auth/login/', user)
          .then((resp) => {
            LocalStorage.set('isAuthenticated', true)
            this.status = 'success'
            this.isAuthenticated = true
            this.hasLoadedOnce = true
            resolve(resp)
          })
          .catch((err) => {
            this.status = 'error'
            this.hasLoadedOnce = true
            LocalStorage.remove('isAuthenticated')
            dataUtil.handleAjaxError(err)
            reject(err)
          })
      })
        .then((result) => {
          // Set user data
          return new Promise((resolve, reject) => {
            api
              .get(`${globalData.API_URL}user/${result.user_id}/`)
              .then((resp) => {
                this.profile = resp.data
                resolve(resp)
              })
              .catch((err) => {
                this.logout()
                this.status = 'error'
                this.profile = {}
                dataUtil.handleAjaxError(err)
                reject(err)
              })
          })
        })
    },
    logout: () => {
      api.post('/auth/logout/').then(() => {
        LocalStorage.remove('isAuthenticated')
        this.isAuthenticated = false
      })
    }
  }
})
