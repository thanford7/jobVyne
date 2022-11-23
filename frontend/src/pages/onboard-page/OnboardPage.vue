<template>
  <div
    class="row justify-center w-100"
    :style="{
      height: '100vh',
      backgroundColor: colorUtil.changeAlpha(colorUtil.getPaletteColor('accent'), 0.5)
    }"
  >
    <ResponsiveWidth>
      <div class="row q-pa-md q-mt-lg justify-center items-center">
        <div class="col-12 text-center">
          <img
            src="../../assets/jobVyneLogoOnly.png" alt="Logo"
            style="max-height: 100px; object-fit: scale-down;"
          />
          <div class="rfs-h2 font-primary">Welcome to JobVyne!</div>
          <div class="rfs-h6">We have a few questions to setup your account</div>
        </div>
      </div>
      <div class="q-pa-md">
        <component
          ref="onboardStep"
          v-bind:is="steps[stepIdx].component"
          v-bind="steps[stepIdx].props"
        >
          <template v-slot:backButton>
            <q-btn
              v-if="stepIdx > 0"
              id="jv-back"
              label="Back"
              size="md"
              flat color="grey-6"
              @click="stepIdx--"
              class="q-ml-sm"
            />
          </template>
          <template v-slot:continueButton>
            <q-btn
              id="jv-forward"
              :label="stepIdx === steps.length - 1 ? 'Finish' : 'Continue'"
              size="md"
              color="primary"
              @click="incrementStep"
            />
          </template>
        </component>
      </div>
    </ResponsiveWidth>
  </div>
</template>

<script>
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import StepBusinessEmail from 'pages/onboard-page/StepBusinessEmail.vue'
import StepName from 'pages/onboard-page/StepName.vue'
import StepSelectEmployer from 'pages/onboard-page/StepSelectEmployer.vue'
import StepUnknownEmployer from 'pages/onboard-page/StepUnknownEmployer.vue'
import StepUserType from 'pages/onboard-page/StepUserType.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'
import {
  USER_TYPES,
  USER_TYPE_EMPLOYER,
  USER_TYPE_CANDIDATE,
  USER_TYPE_EMPLOYEE
} from 'src/utils/user-types.js'

export default {
  name: 'OnboardPage',
  components: {
    ResponsiveWidth,
    StepUserType,
    StepBusinessEmail,
    StepUnknownEmployer,
    StepSelectEmployer,
    StepName
  },
  data () {
    const formData = {
      user_type_bits: 0,
      business_email: null,
      unknown_employer_name: null,
      employer_id: null,
      first_name: null,
      last_name: null
    }
    const userTypesCfg = [
      {
        userTypeBit: USER_TYPES[USER_TYPE_CANDIDATE],
        expanded: false,
        id: 'jv-job-seeker',
        icon: 'fa-solid fa-binoculars',
        title: 'Job Seeker',
        descriptionItems: [
          'Save your job application information for one click applying',
          'Track the status of your applications'
        ]
      },
      {
        userTypeBit: USER_TYPES[USER_TYPE_EMPLOYEE],
        expanded: false,
        id: 'jv-employee',
        icon: 'work',
        title: 'Employee',
        descriptionItems: [
          'Create and post unique job invite links to your social media channels',
          'Track the performance of your links and receive updates on referral bonuses'
        ]
      },
      {
        userTypeBit: USER_TYPES[USER_TYPE_EMPLOYER],
        expanded: false,
        id: 'jv-employer',
        icon: 'business',
        title: 'Employer',
        descriptionItems: [
          'Manage users',
          'Manage administrative settings',
          'Create employer content templates',
          'Manage billing and financials',
          'Set and update employee referral bonus rules'
        ]
      }
    ]
    return {
      stepIdx: 0,
      formData,
      colorUtil,
      userTypesCfg,
      potentialPersonalEmployers: dataUtil.getForceArray(this.employerStore.getEmployersFromDomain(this.user.email)),
      potentialBusinessEmployers: dataUtil.getForceArray(this.employerStore.getEmployersFromDomain(this.user.business_email))
    }
  },
  computed: {
    steps () {
      const all = [
        { component: 'StepUserType', props: { formData: this.formData, userTypesCfg: this.userTypesCfg } }
      ]

      if (dataUtil.isEmptyOrNil(this.user.first_name) || dataUtil.isEmptyOrNil(this.user.last_name)) {
        all.push({
          component: 'StepName',
          props: { formData: this.formData }
        })
      }

      // A business email is used to identify the user's employer if their main email doesn't match with an
      // employer's list of allowed email domains. This can happen when a user uses a personal email to
      // login
      const isNeedsBusinessEmail = (
        (this.formData.user_type_bits & (USER_TYPES[USER_TYPE_EMPLOYEE] | USER_TYPES[USER_TYPE_EMPLOYER])) &&
        !this.user.employer_id &&
        !this.user.business_email &&
        !this.potentialPersonalEmployers.length
      )
      if (isNeedsBusinessEmail) {
        all.push({
          component: 'StepBusinessEmail',
          props: { formData: this.formData, personalEmail: this.user.email }
        })
      }

      // If we still can't identify the user's employer after they provide a business email, we'll
      // need to manually intervene
      if (isNeedsBusinessEmail && !this.potentialBusinessEmployers.length) {
        all.push({
          component: 'StepUnknownEmployer',
          props: { formData: this.formData }
        })
      }

      const potentialEmployers = [...this.potentialPersonalEmployers, ...this.potentialBusinessEmployers]
      if (!this.user.employer_id && potentialEmployers.length > 1) {
        all.push({
          component: 'StepSelectEmployer',
          props: { formData: this.formData, potentialEmployers }
        })
      } else if (!this.user.employer_id && potentialEmployers.length === 1) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.formData.employer_id = potentialEmployers[0].id
      }
      return all
    }
  },
  methods: {
    async incrementStep () {
      const isValidForm = await this.$refs.onboardStep.isValidForm()
      if (!isValidForm) {
        return
      }
      if (this.stepIdx === this.steps.length - 1) {
        await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(this.formData))
        await this.authStore.setUser(true)
        this.$router.push(pagePermissionsUtil.getDefaultLandingPage(this.authStore.propUser))
      } else {
        if (this.formData.business_email) {
          await this.employerStore.setEmployersFromDomain(this.formData.business_email)
          this.potentialBusinessEmployers = this.employerStore.getEmployersFromDomain(this.formData.business_email)
        }
        this.stepIdx++
      }
    }
  },
  async mounted () {
    this.formData.first_name = this.user.first_name
    this.formData.last_name = this.user.last_name
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployersFromDomain(authStore.propUser.email),
        employerStore.setEmployersFromDomain(authStore.propUser.business_email)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const globalStore = useGlobalStore()
    const pageTitle = 'Onboarding Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore,
      employerStore,
      user
    }
  }
}
</script>
