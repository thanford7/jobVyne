<template>
  <q-layout view="hHr lpR fFf">

    <q-header elevated class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md justify-center">
        <q-toolbar-title shrink>
          <img :src="employer?.logo_url" alt="Logo" style="height: 40px; object-fit: scale-down">
        </q-toolbar-title>
      </q-toolbar>
      <ResponsiveWidth class="justify-center">
        <q-tabs align="center" v-model="tab">
          <q-tab name="jobs" label="Jobs"/>
          <q-tab v-if="employerPage && employerPage.is_viewable" name="company" :label="`About ${employer?.name}`"/>
          <q-tab name="me" :label="`About ${profile?.first_name}`"/>
        </q-tabs>
      </ResponsiveWidth>
    </q-header>

    <q-drawer
      v-if="jobApplication"
      v-model="isRightDrawerOpen"
      side="right"
      :breakpoint="600"
      :width="400"
      overlay bordered persistent
    >
      <FormJobApplication :job-application="jobApplication" @closeApplication="closeApplication"/>
      <div v-if="isRightDrawerOpen" class="absolute" style="top: 10px; left: -16px">
        <q-btn
          dense round unelevated
          color="grey-5"
          icon="chevron_right"
          @click="closeApplication()"
        />
      </div>
    </q-drawer>

    <q-page-container class="row justify-center">
      <ResponsiveWidth>
        <BannerMessage/>
        <q-page v-if="!isLoading" padding>
          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="jobs">
              <div class="row">
                <div class="col-12">
                  <div v-for="job in jobs" :key="job.id" class="q-mb-md">
                    <q-card :class="(jobApplication && jobApplication.id === job.id) ? 'q-card--selected' : ''">
                      <div v-if="getJobApplication(job.id)" class="application-date">
                        Applied on {{ dateTimeUtil.getShortDate(getJobApplication(job.id).created_dt) }}
                      </div>
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
                      <q-card-actions v-if="!getJobApplication(job.id)">
                        <q-btn ripple unelevated color="accent" label="Apply" @click="openApplication(job.id)"/>
                      </q-card-actions>
                    </q-card>
                  </div>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel v-if="employerPage && employerPage.is_viewable" name="company">
              <div class="row">
                <div class="col-12">
                  <EmployerProfile/>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel name="me">
              <div class="row">
                <div class="col-12">Me placeholder</div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </q-page>
      </ResponsiveWidth>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import EmployerProfile from 'pages/jobs-page/EmployerProfile.vue'
import { useEmployerStore } from 'stores/employer-store.js'
import { ref } from 'vue'
import BannerMessage from 'components/BannerMessage.vue'
import CustomFooter from 'components/CustomFooter.vue'
import locationUtil from 'src/utils/location'
import dataUtil from 'src/utils/data'
import { useAuthStore } from 'stores/auth-store'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useGlobalStore } from 'stores/global-store'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import DialogJobApp from 'components/dialogs/DialogJobApp.vue'
import dateTimeUtil from 'src/utils/datetime'
import { storeToRefs } from 'pinia/dist/pinia'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

export default {
  data () {
    return {
      tab: 'jobs',
      jobs: null,
      employer: null,
      profile: null,
      isLoading: true,
      jobApplication: null,
      dateTimeUtil
    }
  },
  components: { EmployerProfile, ResponsiveWidth, FormJobApplication, CustomFooter, BannerMessage },
  computed: {
    employerPage () {
      return this.employerStore.getEmployerPage(this.user.employer_id)
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getSalaryRange: dataUtil.getSalaryRange.bind(dataUtil),
    async closeApplication () {
      this.isRightDrawerOpen = false
      this.jobApplication = null
      await this.$router.replace({ name: this.$route.name, query: {} })
    },
    async openApplication (jobId) {
      this.jobApplication = this.jobs.find((j) => j.id === jobId)
      await this.$router.replace({ name: this.$route.name, query: { jobId } })
      if (window.innerWidth < 600) {
        this.openJobAppModal(this.jobApplication).onDismiss(() => this.closeApplication())
      } else {
        this.isRightDrawerOpen = true
      }
    },
    getJobApplication (jobId) {
      if (!this.applications) {
        return null
      }
      return this.applications.find((app) => app.employer_job.id === jobId)
    }
  },
  async mounted () {
    const resp = await this.$api.get(`social-link-jobs/${this.$route.params.filterId}`)
    const { jobs, employer, profile } = resp.data
    this.jobs = jobs
    this.employer = employer
    this.profile = profile

    const { jobId } = dataUtil.getQueryParams()
    if (jobId) {
      this.openApplication(parseInt(jobId))
    }

    this.isLoading = false
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployerPage(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const isRightDrawerOpen = ref(false)
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user, applications } = storeToRefs(authStore)

    const pageTitle = 'Jobs'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
    const $q = useQuasar()
    const openJobAppModal = (jobApplication) => {
      return $q.dialog({
        component: DialogJobApp,
        componentProps: { jobApplication },
        noRouteDismiss: true
      })
    }

    return {
      user,
      applications,
      isRightDrawerOpen,
      openJobAppModal,
      employerStore: useEmployerStore()
    }
  }
}
</script>

<style lang="scss" scoped>
.application-date {
  padding: 8px;
  color: $white;
  background-color: map-get($brand-color-map, 'primary');
}
</style>
