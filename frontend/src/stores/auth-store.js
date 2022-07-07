import { defineStore } from 'pinia'
import { getAjaxFormData } from 'src/utils/requests'
import { LocalStorage } from 'quasar'

// Keep in sync with backend user model
const USER_TYPES = {
  USER_TYPE_ADMIN: 0x1,
  USER_TYPE_CANDIDATE: 0x2,
  USER_TYPE_EMPLOYEE: 0x4,
  USER_TYPE_INFLUENCER: 0x8,
  USER_TYPE_EMPLOYER: 0x10
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: LocalStorage.getItem('isAuthenticated') || false,
    profile: LocalStorage.getItem('profile') || {}
  }),
  getters: {
    getProfile: (state) => state.profile,
    getIsAdmin: (state) => state?.profile?.user_type_bits & USER_TYPES.USER_TYPE_ADMIN,
    getIsCandidate: (state) => state?.profile?.user_type_bits & USER_TYPES.USER_TYPE_CANDIDATE,
    getIsEmployee: (state) => state?.profile?.user_type_bits & USER_TYPES.USER_TYPE_EMPLOYEE,
    getIsInfluencer: (state) => state?.profile?.user_type_bits & USER_TYPES.USER_TYPE_INFLUENCER,
    getIsEmployer: (state) => state?.profile?.user_type_bits & USER_TYPES.USER_TYPE_EMPLOYER
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
        throw err
      }
      await this.setUserProfile(resp.data.user_id)
    },
    async logout () {
      await this.$api.post('auth/logout/')
      this.updateStatus(false)
      this.profile = {}
      this.$router.push('/')
    },
    async setUserProfile (userId) {
      const userResp = await this.$api.get(`user/${userId}/`)
      this.profile = userResp.data
      LocalStorage.set('profile', userResp.data)
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
