import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'

// Keep in sync with backend user model
export const USER_TYPE_ADMIN = 'Admin'
export const USER_TYPE_CANDIDATE = 'Candidate'
export const USER_TYPE_EMPLOYEE = 'Employee'
export const USER_TYPE_INFLUENCER = 'Influencer'
export const USER_TYPE_EMPLOYER = 'Employer'

export const USER_TYPES = {
  [USER_TYPE_ADMIN]: 0x1,
  [USER_TYPE_CANDIDATE]: 0x2,
  [USER_TYPE_EMPLOYEE]: 0x4,
  [USER_TYPE_INFLUENCER]: 0x8,
  [USER_TYPE_EMPLOYER]: 0x10
}

/**
 * The bulk of authentication is handled in router-guards.js where:
 * (1) Check if user is authenticated
 *
 * authStore is used to:
 * (2) Logout
 * (3) Set user and access all properties
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {},
    applications: []
  }),
  getters: {
    propIsAuthenticated: (state) => state.user && !dataUtil.isEmpty(state.user),
    propUser: (state) => state.user,
    propUserTypeBits: (state) => state?.user?.user_type_bits,
    propIsAdmin: (state) => state?.user?.user_type_bits & USER_TYPES.Admin,
    propIsCandidate: (state) => state?.user?.user_type_bits & USER_TYPES.Candidate,
    propIsEmployee: (state) => state?.user?.user_type_bits & USER_TYPES.Employee,
    propIsInfluencer: (state) => state?.user?.user_type_bits & USER_TYPES.Influencer,
    propIsEmployer: (state) => state?.user?.user_type_bits & USER_TYPES.Employer,
    propUserTypeBitsList: (state) => {
      return Object.values(USER_TYPES).reduce((userBitsList, userBit) => {
        const flippedBit = userBit & state?.user?.user_type_bits
        if (flippedBit) {
          userBitsList.push(flippedBit)
        }
        return userBitsList
      }, [])
    }
  },
  actions: {
    async logout () {
      await this.$api.post('auth/logout/')
      this.user = {}
      this.$router.push('/')
    },
    async setUser (isForce = false) {
      if (isForce || !this.user || dataUtil.isEmpty(this.user)) {
        const resp = await this.$api.get('auth/check-auth/')
        this.user = resp.data || {}
        if (!dataUtil.isEmpty(this.user)) {
          await this.setApplications(this.user, isForce)
        }
      }
    },
    async setApplications (user, isForce = false) {
      if (!user) {
        return
      }
      if (isForce || !this.applications.length) {
        const resp = await this.$api.get('job-application/', {
          params: { user_id: user.id }
        })
        this.applications = resp.data
      }
    }
  }
})
