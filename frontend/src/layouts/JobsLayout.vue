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
      v-model="rightDrawerOpen"
      side="right"
      overlay bordered :width="400"
    >
      <template v-if="!isApplicationSaved">
        <div class="q-pa-sm bg-primary text-white">
          <div class="text-h6 text-center">Apply to {{ applicationJob.job_title }}</div>
        </div>
        <div class="q-pa-sm q-mt-sm">
          <q-form
            @submit="saveApplication"
            class="q-gutter-xs"
          >
            <q-input
              filled
              v-model="formData.firstName"
              label="First name"
              lazy-rules
              :rules="[ val => val && val.length > 0 || 'First name is required']"
            />
            <q-input
              filled
              v-model="formData.lastName"
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
              :rules="[ val => val && val.length > 0 && isGoodEmail(val) || 'A valid email is required']"
            />
            <q-input
              filled
              v-model="formData.phoneNumber"
              type="tel"
              label="Phone number*"
              lazy-rules
              :rules="[ val => !val || !val.length || !isGoodPhoneNumber(val) || 'The phone number must be valid']"
            />
            <q-input
              filled
              v-model="formData.linkedInUrl"
              type="url"
              label="LinkedIn URL*"
              hint="www.linkedin.com/in/{your profile id}"
              lazy-rules
              :rules="[ val => !val || !val.length || !isGoodLinkedInUrl(val)  || 'The LinkedIn URL must be valid']"
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
      <template v-else-if="true || !authStore.isAuthenticated">
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
              'Message with employees and employers'
            ]"
          />
        </div>
      </template>
      <div v-if="rightDrawerOpen" class="absolute" style="top: 10px; left: -16px">
        <q-btn
          dense
          round
          unelevated
          color="grey-5"
          icon="chevron_right"
          @click="rightDrawerOpen=false"
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
                    <q-card>
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

const formDataTemplate = {
  firstName: null,
  lastName: null,
  email: null,
  phoneNumber: null,
  linkedInUrl: null,
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
      isApplicationSaved: true,
      applicationJob: null,
      formData: { ...formDataTemplate }
    }
  },
  components: { ListIcon, CustomFooter, BannerMessage },
  computed: {
    applicationTemplate () {
      const applicantProfile = this.authStore.getProfile
      if (!applicantProfile) {
        return null
      }
      return applicantProfile.applicationTemplate
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getSalaryRange: dataUtil.getSalaryRange.bind(dataUtil),
    isGoodEmail: formUtil.isGoodEmail,
    isGoodLinkedInUrl: formUtil.isGoodLinkedInUrl,
    isGoodPhoneNumber: formUtil.isGoodPhoneNumber,
    openApplication (jobId) {
      this.applicationJob = this.jobs.find((j) => j.id === jobId)
      this.rightDrawerOpen = true
      if (this.applicationTemplate) {
        Object.assign(this.formData, this.applicationTemplate)
      }
    },
    saveApplication () {
      // TODO: Add backend and axios call
      this.isApplicationSaved = true
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
  setup () {
    const rightDrawerOpen = ref(false)
    const authStore = useAuthStore()

    return {
      authStore,
      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  }
}
</script>
