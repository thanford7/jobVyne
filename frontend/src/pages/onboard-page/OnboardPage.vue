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
        <q-card>
          <q-form ref="form">
            <q-card-section>
              <div class="row q-gutter-y-md q-mt-sm">
                <template v-if="!user.employer_id && !this.potentialEmployers?.length">
                  <div v-if="!user.business_email">
                    We can't find a current employer connected with the domain from your email
                    address ({{ user.email }}). If you used your personal email to login, please
                    enter your business email here. Otherwise please contact support@jobvyne.com for help.
                  </div>
                  <div v-else>
                    We can't find a current employer connected with the domain from your email
                    address ({{ user.email }}) or your business email ({{ user.business_email }}).
                    If you entered your business email incorrectly, please update it.
                    Otherwise please contact support@jobvyne.com for help.
                  </div>
                  <div class="col-12">
                    <EmailInput
                      v-model="formData.business_email"
                      label="Business email" autofocus
                      :additional-rules="[
                        val => val !== user.email || 'Business email must be different than personal email'
                      ]"
                    />
                  </div>
                </template>
                <template v-else>
                  <div v-if="!user.employer_id" class="col-12">
                    <q-select
                      id="jv-employer-sel"
                      filled emit-value map-options autofocus
                      v-model="formData.employer_id"
                      :options="potentialEmployers"
                      autocomplete="name"
                      option-value="id"
                      option-label="name"
                      label="Employer"
                      lazy-rules
                      :rules="[val => val || 'Please select an option']"
                    />
                  </div>
                  <div class="col-12 col-md-6 q-pr-md-sm">
                    <q-input
                      v-model="formData.first_name"
                      class="jv-fname" filled
                      label="First name" lazy-rules
                      :rules="[
                      val => val && val.length > 0 || 'First name is required'
                    ]"
                    />
                  </div>
                  <div class="col-12 col-md-6 q-pl-md-sm">
                    <q-input
                      v-model="formData.last_name"
                      class="jv-lname" filled
                      label="Last name" lazy-rules
                      :rules="[
                      val => val && val.length > 0 || 'Last name is required'
                    ]"
                    />
                  </div>
                  <div class="col-12 col-md-6 q-pr-md-sm">
                    <q-input
                      v-model="formData.job_title"
                      class="jv-job-title" filled
                      label="Job title" lazy-rules
                      :rules="[
                      val => val && val.length > 0 || 'Job title is required'
                    ]"
                    />
                  </div>
                  <div class="col-12 col-md-6 q-pl-md-sm">
                    <SelectJobProfession v-model="formData.profession_id" :is-multi="false" :is-required="true"/>
                  </div>
                </template>
              </div>
            </q-card-section>
            <q-card-actions align="right">
              <q-btn color="primary" label="Save" class="w-100" @click="saveUser()"/>
            </q-card-actions>
          </q-form>
        </q-card>
      </div>
    </ResponsiveWidth>
  </div>
</template>

<script>
import EmailInput from 'components/inputs/EmailInput.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { USER_TYPE_EMPLOYEE, USER_TYPES } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'OnboardPage',
  components: {
    SelectJobProfession,
    EmailInput,
    ResponsiveWidth
  },
  data () {
    return {
      stepIdx: 0,
      formData: {
        business_email: null,
        employer_id: null,
        first_name: null,
        last_name: null,
        profession_id: null,
        job_title: null
      },
      colorUtil,
      potentialEmployers: [],
      authStore: useAuthStore(),
      employerStore: useEmployerStore()
    }
  },
  methods: {
    async updateEmployers () {
      await Promise.all([
        this.employerStore.setEmployersFromDomain(this.user.email),
        this.employerStore.setEmployersFromDomain(this.user.business_email)
      ])
      const potentialPersonalEmployers = dataUtil.getForceArray(this.employerStore.getEmployersFromDomain(this.user.email))
      const potentialBusinessEmployers = dataUtil.getForceArray(this.employerStore.getEmployersFromDomain(this.user.business_email))
      this.potentialEmployers = [...potentialPersonalEmployers, ...potentialBusinessEmployers]
    },
    async saveUser () {
      const isGoodForm = await this.$refs.form.validate()
      if (!isGoodForm) {
        return
      }
      if (this.formData.employer_id) {
        this.formData.user_type_bits = USER_TYPES[USER_TYPE_EMPLOYEE]
      }
      await this.$api.put(`user/${this.user.id}/`, getAjaxFormData(this.formData))
      await this.authStore.setUser(true)
      if (!this.user.employer_id) {
        await this.updateEmployers()
      } else {
        this.$router.push(pagePermissionsUtil.getDefaultLandingPage(this.authStore.propUser))
      }
    }
  },
  async mounted () {
    Loading.show()

    await this.authStore.setUser().then(() => {
      return this.updateEmployers()
    }).finally(() => {
      Loading.hide()
    })
    Object.assign(this.formData, dataUtil.pick(this.user, Object.keys(this.formData)))
  },
  setup () {
    const { user } = storeToRefs(useAuthStore())

    const globalStore = useGlobalStore()
    const pageTitle = 'Onboarding Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return { user }
  }
}
</script>
