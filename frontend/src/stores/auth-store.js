import { defineStore } from 'pinia'
import { getAjaxFormData } from 'src/utils/requests'
import dataUtil from 'src/utils/data'

// Keep in sync with backend user model
export const USER_TYPES = {
  USER_TYPE_ADMIN: 0x1,
  USER_TYPE_CANDIDATE: 0x2,
  USER_TYPE_EMPLOYEE: 0x4,
  USER_TYPE_INFLUENCER: 0x8,
  USER_TYPE_EMPLOYER: 0x10
}

/**
 * The bulk of authentication is handled in router-guards.js where:
 * (1) Check if user is authenticated
 *
 * authStore is used to:
 * (1) Login
 * (2) Logout
 * (3) Set user and access all properties
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {}
  }),
  getters: {
    propIsAuthenticated: (state) => state.user && !dataUtil.isEmpty(state.user),
    propUser: (state) => state.user,
    propIsAdmin: (state) => state?.user?.user_type_bits & USER_TYPES.USER_TYPE_ADMIN,
    propIsCandidate: (state) => state?.user?.user_type_bits & USER_TYPES.USER_TYPE_CANDIDATE,
    propIsEmployee: (state) => state?.user?.user_type_bits & USER_TYPES.USER_TYPE_EMPLOYEE,
    propIsInfluencer: (state) => state?.user?.user_type_bits & USER_TYPES.USER_TYPE_INFLUENCER,
    propIsEmployer: (state) => state?.user?.user_type_bits & USER_TYPES.USER_TYPE_EMPLOYER
  },
  actions: {
    async login (userData) {
      // TODO: Add loading indicator
      await this.$api.post('auth/login/', getAjaxFormData(userData))
      this.$router.push('/dashboard')
    },
    async logout () {
      await this.$api.post('auth/logout/')
      this.user = {}
      this.$router.push('/')
    },
    async setUser () {
      if (!this.user || dataUtil.isEmpty(this.user)) {
        const resp = await this.$api.get('auth/check-auth/')
        this.user = resp.data || {}
      }
    }
  }
})
