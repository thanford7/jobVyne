import { defineStore } from 'pinia'
import dataUtil from 'src/utils/data'
import { USER_TYPES } from 'src/utils/user-types'
import { getAjaxFormData } from 'src/utils/requests'

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
    applications: [],
    employeeQuestions: {} // employerId: [<question1>, <question2>, ...]
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
    async logout (redirect = '/') {
      await this.$api.post('auth/logout/')
      if (redirect) {
        await this.$router.push(redirect)
      }
      this.user = {}
    },
    async setUser (isForce = false) {
      if (isForce || !this.user || dataUtil.isEmpty(this.user)) {
        const resp = await this.$api.get('auth/check-auth/')
        this.user = resp?.data?.user || {}
      }
    },
    async setApplications (user, isForce = false) {
      if (!user || dataUtil.isEmpty(user)) {
        this.applications = []
        return
      }
      if (isForce || !this.applications.length) {
        const resp = await this.$api.get('job-application/', {
          params: { user_id: user.id }
        })
        this.applications = resp.data
      }
    },
    async setUserEmployeeQuestions (employerId) {
      const resp = await this.$api.get('employee-questions/', {
        params: { employer_id: employerId }
      })
      this.employeeQuestions[employerId] = resp.data
    },
    getHasPermission (permissionName, employerId = null) {
      employerId = employerId || this.user.employer_id
      if (!this.user || !this.user.permissions_by_employer[employerId]) {
        return false
      }
      return this.user.permissions_by_employer[employerId].includes(permissionName)
    },
    getUserEmployeeQuestions (employerId) {
      return this.employeeQuestions[employerId]
    },
    executeIfCaptchaValid (action, successFn, failureFn, alwaysFn = null) {
      // eslint-disable-next-line no-undef
      grecaptcha.enterprise.ready(async () => {
        // eslint-disable-next-line no-undef
        const token = await grecaptcha.enterprise.execute(process.env.GOOGLE_CAPTCHA_KEY, { action })
        const resp = await this.$api.post('auth/validate-captcha/', getAjaxFormData({ token, action }))
        if (resp?.data?.score) {
          successFn()
        } else {
          failureFn()
        }
        if (alwaysFn) {
          alwaysFn()
        }
      })
    }
  }
})
