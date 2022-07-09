<template>
  <q-layout view="hHr lpR fFf">

    <q-header elevated class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md justify-center">
        <q-toolbar-title shrink>
          <img :src="employer?.logo" alt="Logo" style="height: 40px; object-fit: scale-down">
        </q-toolbar-title>
      </q-toolbar>
      <div class="col-12 col-md-11 col-lg-8 justify-center">
        <q-tabs align="center" v-model="tab">
          <q-tab name="jobs" label="Jobs"/>
          <q-tab name="company" :label="`About ${employer?.name}`"/>
          <q-tab name="me" :label="`About ${profile?.first_name}`"/>
        </q-tabs>
      </div>
    </q-header>

    <q-drawer
      v-if="applicationJob"
      v-model="isRightDrawerOpen"
      side="right"
      overlay bordered :width="400"
    >
      <template v-if="!isApplicationSaved">
        <div class="q-pa-sm bg-primary text-white">
          <div class="text-h6 text-center">Apply to {{ applicationJob.job_title }}</div>
        </div>
        <div v-if="!authStore.propIsAuthenticated">
          Have an account? Login to auto-populate the form
          TODO
        </div>
        <div class="q-pa-sm q-mt-sm">
          <q-form
            @submit="saveApplication"
            class="q-gutter-xs"
          >
            <q-input
              filled
              v-model="formData.first_name"
              label="First name"
              lazy-rules
              :rules="[ val => val && val.length > 0 || 'First name is required']"
            />
            <q-input
              filled
              v-model="formData.last_name"
              label="Last name"
              lazy-rules
              :rules="[ val => val && val.length > 0 || 'Last name is required']"
            />
            <q-input
              filled
              v-model="formData.email"
              type="email"
              label="Email"
              lazy-rules
              :rules="[ val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'A valid email is required']"
            />
            <q-input
              filled
              v-model="formData.phone_number"
              type="tel"
              label="Phone number*"
              lazy-rules
              :rules="[ val => !val || !val.length || formUtil.isGoodPhoneNumber(val) || 'The phone number must be valid']"
            />
            <q-input
              filled
              v-model="formData.linkedin_url"
              type="url"
              label="LinkedIn URL*"
              hint="www.linkedin.com/in/{your profile id}"
              lazy-rules
              :rules="[ val => !val || !val.length || formUtil.isGoodLinkedInUrl(val)  || 'The LinkedIn URL must be valid']"
            />
            <q-file
              filled bottom-slots
              v-model="formData.resume"
              label="Resume"
              class="q-mb-none"
            />
            <div class="text-small text-gray-3">
              *Optional
            </div>

            <div>
              <q-btn label="Submit application" type="submit" color="accent"/>
            </div>
          </q-form>
        </div>
      </template>
      <template v-else-if="!authStore.propIsAuthenticated">
        <div class="q-pa-sm bg-primary text-white">
          <div class="text-h6 text-center">Create an account</div>
        </div>
        <div class="q-pa-sm q-mt-sm">
          <div class="text-bold">Create an account and save time</div>
          <ListIcon
            color="primary"
            icon-name="thumb_up"
            :items="[
              'One click application submission',
              'Message with employees and employers',
              'Track the jobs you\'ve already applied to'
            ]"
          />
          <q-separator/>
          <div class="q-mt-md">
            <AuthEmailForm :is-create="true"/>
            <SeparatorWithText>or</SeparatorWithText>
            <AuthSocialButtons :is-create="true"/>
          </div>
        </div>
      </template>
      <div v-if="isRightDrawerOpen" class="absolute" style="top: 10px; left: -16px">
        <q-btn
          dense
          round
          unelevated
          color="grey-5"
          icon="chevron_right"
          @click="closeRightDrawer()"
        />
      </div>
    </q-drawer>

    <q-page-container class="row justify-center">
      <div class="col-12 col-md-11 col-lg-8">
        <BannerMessage/>
        <q-page v-if="!isLoading" padding>
          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="jobs">
              <div class="row">
                <div class="col-12">
                  <div v-for="job in jobs" :key="job.id" class="q-mb-md">
                    <q-card :class="(applicationJob && applicationJob.id === job.id) ? 'q-card--selected' : ''">
                      <q-card-section>
                        <h6>{{ job.job_title }}</h6>
                        <div>
                          <q-chip color="grey-7" text-color="white" size="md" icon="domain">
                            {{ job.job_department }}
                          </q-chip>
                          <q-chip color="grey-7" text-color="white" size="md" icon="place">
                            {{ getFullLocation(job) }}
                          </q-chip>
                          <q-chip v-if="job.is_remote" color="grey-7" text-color="white" size="md" icon="laptop">
                            Remote
                          </q-chip>
                          <q-chip color="grey-7" text-color="white" size="md" icon="schedule">
                            {{ (job.is_full_time) ? 'Full-Time' : 'Part-Time' }}
                          </q-chip>
                        </div>
                        <div>
                          <q-chip v-if="getSalaryRange(job.salary_floor, job.salary_ceiling)" color="grey-7"
                                  text-color="white" size="md" icon="laptop">
                            {{ getSalaryRange(job.salary_floor, job.salary_ceiling) }}
                          </q-chip>
                        </div>
                        <q-separator class="q-mt-sm"/>
                        <p>
                          {{ job.job_description }}
                        </p>
                      </q-card-section>
                      <q-separator dark/>
                      <q-card-actions>
                        <q-btn unelevated color="accent" label="Apply" @click="openApplication(job.id)"/>
                      </q-card-actions>
                    </q-card>
                  </div>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel name="company">
              <div class="row">
                <div class="col-12">Company placeholder</div>
              </div>
            </q-tab-panel>
            <q-tab-panel name="me">
              <div class="row">
                <div class="col-12">Me placeholder</div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-page>
      </div>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import { ref } from 'vue'
import BannerMessage from 'components/BannerMessage.vue'
import CustomFooter from 'components/CustomFooter.vue'
import locationUtil from 'src/utils/location'
import dataUtil from 'src/utils/data'
import formUtil from 'src/utils/form'
import { useAuthStore } from 'stores/auth-store'
import ListIcon from 'components/ListIcon.vue'
import AuthEmailForm from 'components/AuthEmailForm.vue'
import AuthSocialButtons from 'components/AuthSocialButtons.vue'
import SeparatorWithText from 'components/SeparatorWithText.vue'
import { getAjaxFormData } from 'src/utils/requests'
import { Loading, useMeta } from 'quasar'
import { useGlobalStore } from 'stores/global-store'

const formDataTemplate = {
  first_name: null,
  last_name: null,
  email: null,
  phone_number: null,
  linkedin_url: null,
  resume: null
}

export default {
  data () {
    return {
      tab: 'jobs',
      jobs: null,
      employer: null,
      profile: null,
      isLoading: true,
      isApplicationSaved: false,
      applicationJob: null,
      formData: { ...formDataTemplate },
      formUtil
    }
  },
  components: { SeparatorWithText, AuthSocialButtons, AuthEmailForm, ListIcon, CustomFooter, BannerMessage },
  computed: {
    applicantProfile () {
      return this.authStore.propUser
    },
    applicationTemplate () {
      if (!this.applicantProfile) {
        return null
      }
      return this.applicantProfile.applicationTemplate
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getSalaryRange: dataUtil.getSalaryRange.bind(dataUtil),
    closeRightDrawer () {
      this.isRightDrawerOpen = false
      this.applicationJob = null
    },
    openApplication (jobId) {
      this.applicationJob = this.jobs.find((j) => j.id === jobId)
      this.isRightDrawerOpen = true
      Object.assign(
        this.formData,
        (this.applicantProfile) ? dataUtil.pick(this.applicantProfile, ['first_name', 'last_name', 'email']) : {},
        this.applicationTemplate || {}
      )
    },
    async saveApplication () {
      await this.$api.post('submit-application', getAjaxFormData(this.formData, ['resume']))
      this.isApplicationSaved = true
      // Leave the drawer open to allow user to create an account if they don't have one
      if (this.authStore.propIsAuthenticated) {
        this.closeRightDrawer()
      }
    }
  },
  async mounted () {
    const resp = await this.$api.get(`social-link-jobs/${this.$route.params.jobId}`)
    const { jobs, employer, profile } = resp.data
    this.jobs = jobs
    this.employer = employer
    this.profile = profile
    this.isLoading = false
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()
    authStore.setUser().finally(() => Loading.hide())
  },
  setup () {
    const isRightDrawerOpen = ref(false)
    const globalStore = useGlobalStore()

    const pageTitle = 'Jobs'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle(pageTitle)
    }
    useMeta(metaData)

    return {
      authStore: useAuthStore(),
      isRightDrawerOpen,
      toggleRightDrawer () {
        isRightDrawerOpen.value = !isRightDrawerOpen.value
      }
    }
  }
}
</script>
