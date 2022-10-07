<template>
  <q-layout view="hHr lpR fFf">

    <q-header v-if="isLoaded" elevated class="bg-white text-primary justify-center row">
      <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
        <q-toolbar-title shrink>
          <img :src="employer?.logo_url" alt="Logo" style="height: 40px; object-fit: scale-down">
        </q-toolbar-title>
      </q-toolbar>
      <ResponsiveWidth class="justify-center">
        <q-tabs align="center" v-model="tab" :style="getTabStyle()">
          <q-tab name="jobs" label="Jobs"/>
          <q-tab v-if="employerPage && employerPage.is_viewable" name="company" :label="`About ${employer?.name}`"/>
          <q-tab v-if="isShowEmployeeProfile" name="me" :label="`About ${profile?.first_name}`"/>
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
      <FormJobApplication
        :job-application="jobApplication"
        :employer="employer"
        @closeApplication="closeApplication"
      />
      <div v-if="isRightDrawerOpen" class="absolute" style="top: 10px; left: -16px">
        <q-btn
          dense round unelevated
          color="grey-5"
          icon="chevron_right"
          @click="closeApplication()"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <ResponsiveWidth>
        <BannerMessage/>
      </ResponsiveWidth>
      <q-page v-if="isLoaded" class="scroll">
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="jobs">
            <div class="row justify-center">
              <ResponsiveWidth>
                <q-page padding>
                  <div v-if="isActiveEmployer" class="row">
                    <div class="col-12">
                      <div v-if="!jobs.length" class="q-mb-md">
                        <q-card class="q-pa-lg" :style="getSelectedCardStyle(job)">
                          <div class="text-h6 text-center">No current job openings</div>
                        </q-card>
                      </div>
                      <div v-for="job in jobs" :key="job.id" class="q-mb-md">
                        <q-card :style="getSelectedCardStyle(job)" :id="`job-${job.id}`">
                          <div v-if="getJobApplication(job.id)" class="application-date" :style="getHeaderStyle()">
                            Applied on {{ dateTimeUtil.getShortDate(getJobApplication(job.id).created_dt) }}
                          </div>
                          <q-card-section>
                            <h6 class="q-mb-none">{{ job.job_title }}</h6>
                            <div class="text-grey-7 q-mb-sm">
                              Posted on: {{ dateTimeUtil.getShortDate(job.open_date) }}
                            </div>
                            <div>
                              <q-chip color="grey-7" text-color="white" size="md" icon="domain">
                                {{ job.job_department }}
                              </q-chip>
                              <template v-if="job.locations.length > 1">
                                <CustomTooltip>
                                  <template v-slot:icon>
                                    <q-chip
                                      color="grey-7" text-color="white" size="md" icon="place"
                                    >
                                      Multiple locations
                                    </q-chip>
                                  </template>
                                  <ul>
                                    <li v-for="location in job.locations">
                                      {{ getFullLocation(location) }}
                                    </li>
                                  </ul>
                                </CustomTooltip>
                              </template>
                              <q-chip
                                v-else-if="job.locations.length"
                                color="grey-7" text-color="white" size="md" icon="place"
                              >
                                {{ getFullLocation(job.locations[0]) }}
                              </q-chip>
                              <q-chip v-if="job.is_remote" color="grey-7" text-color="white" size="md" icon="laptop">
                                Remote
                              </q-chip>
                              <q-chip color="grey-7" text-color="white" size="md" icon="schedule">
                                {{ job.employment_type }}
                              </q-chip>
                              <q-chip v-if="getSalaryRange(job.salary_floor, job.salary_ceiling)" color="grey-7"
                                      text-color="white" size="md" icon="attach_money">
                                {{ getSalaryRange(job.salary_floor, job.salary_ceiling) }}
                              </q-chip>
                            </div>
                            <q-separator class="q-mt-sm"/>
                            <div class="q-pa-sm" v-html="formUtil.sanitizeHtml(job.job_description)"></div>
                          </q-card-section>
                          <q-separator dark/>
                          <q-card-actions v-if="!getJobApplication(job.id)">
                            <q-btn
                              ripple unelevated
                              label="Apply"
                              :style="getButtonStyle()"
                              @click="openApplication($event, job.id)"
                            />
                          </q-card-actions>
                        </q-card>
                      </div>
                      <q-pagination
                        v-if="jobPagesCount > 1"
                        v-model="pageNumber"
                        :max-pages="5"
                        :max="jobPagesCount"
                        direction-links
                      />
                    </div>
                  </div>
                  <div v-else class="row justify-center items-center" style="height: 50vh">
                    <div class="col-6">
                      <q-card class="bg-primary text-white">
                        <q-card-section class="flex justify-center">
                          <q-icon name="power_off" size="80px"/>
                        </q-card-section>
                        <q-card-section>
                          <div class="text-h6 text-center">
                            {{ employer.name }} no longer has an active JobVyne account. If you wish to
                            view and apply for jobs, please visit their
                            <a v-if="employer.company_jobs_page_url" :href="employer.company_jobs_page_url"
                               target="_blank">
                              jobs page
                            </a>
                            <span v-else>jobs page</span>
                          </div>
                        </q-card-section>
                      </q-card>
                    </div>
                  </div>
                </q-page>
              </ResponsiveWidth>
            </div>
          </q-tab-panel>
          <q-tab-panel
            v-if="employerPage && employerPage.is_viewable"
            name="company"
            class="q-pa-none"
          >
            <div class="row">
              <div class="col-12">
                <EmployerProfile :employer-id="employer.id"/>
              </div>
            </div>
          </q-tab-panel>
          <q-tab-panel name="me" v-if="isShowEmployeeProfile" class="q-pa-none">
            <div class="row justify-center q-px-xl q-pt-xl bg-grey-3">
              <div class="col-12 col-md-4 q-pr-md-md q-mb-md q-mb-md-none">
                <div class="flex items-center">
                  <img
                    v-if="profile.profile_picture_url"
                    :src="profile.profile_picture_url"
                    alt="Profile picture"
                    class="q-mr-md"
                    style="height: 150px; object-fit: scale-down; border-radius: 10px; float: left;"
                  >
                  <div class="q-gutter-y-sm">
                    <div class="text-h6 text-bold">{{ profile.first_name }} {{ profile.last_name }}</div>
                    <div>{{ profile.job_title }}</div>
                    <div v-if="profile.home_location">{{ locationUtil.getFullLocation(profile.home_location) }}</div>
                    <div v-if="profile.employment_start_date">
                      {{ dataUtil.pluralize('year', employmentYears) }} at {{ employer.name }}
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6 q-pl-md-md">
                <div v-for="response in profile.profile_responses">
                  <div class="text-h6">{{ response.question }}</div>
                  <div class="q-mt-sm q-mb-md">{{ response.response }}</div>
                </div>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-page>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import EmployerProfile from 'pages/jobs-page/EmployerProfile.vue'
import colorUtil from 'src/utils/color.js'
import formUtil from 'src/utils/form.js'
import scrollUtil from 'src/utils/scroll.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useUserStore } from 'stores/user-store.js'
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
      tab: this.$route?.params?.tab || 'jobs',
      jobs: null,
      employer: null,
      employerPage: null,
      profile: null,
      isLoaded: false,
      isActiveEmployer: null,
      jobApplication: null,
      jobPagesCount: null,
      pageNumber: 1,
      dataUtil,
      dateTimeUtil,
      formUtil,
      locationUtil
    }
  },
  components: { CustomTooltip, EmployerProfile, ResponsiveWidth, FormJobApplication, CustomFooter, BannerMessage },
  computed: {
    employmentYears () {
      if (!this.profile.employment_start_date) {
        return null
      }
      return dateTimeUtil.getDateDifference(this.profile.employment_start_date, dateTimeUtil.today(), 'years')
    },
    isShowEmployeeProfile () {
      return Boolean(this.profile && this.profile.is_profile_viewable && this.profile.profile_responses.length)
    }
  },
  watch: {
    pageNumber: {
      async handler () {
        await this.loadData()
      }
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
    async openApplication (e, jobId) {
      this.jobApplication = this.jobs.find((j) => j.id === jobId)
      await this.$router.replace({ name: this.$route.name, query: { jobId } })
      if (window.innerWidth < 600) {
        this.openJobAppModal(this.jobApplication).onDismiss(() => this.closeApplication())
      } else {
        this.isRightDrawerOpen = true
      }
      scrollUtil.scrollToElement(document.getElementById(`job-${jobId}`))
    },
    async loadData () {
      Loading.show()
      const resp = await this.$api.get(`social-link-jobs/${this.$route.params.filterId}`, {
        params: { page_count: this.pageNumber }
      })
      const { jobs, employer, total_page_count: totalPageCount, owner_id: ownerId } = resp.data
      await this.employerStore.setEmployerSubscription(employer.id)
      const { is_active: isActiveEmployer } = this.employerStore.getEmployerSubscription(employer.id)
      this.isActiveEmployer = isActiveEmployer
      this.jobs = (isActiveEmployer) ? jobs : []
      this.employer = employer

      await this.userStore.setUserProfile(ownerId)
      this.profile = this.userStore.getUserProfile(ownerId)
      this.jobPagesCount = totalPageCount
      Loading.hide()
    },
    getJobApplication (jobId) {
      if (!this.applications) {
        return null
      }
      return this.applications.find((app) => app.employer_job.id === jobId)
    },
    getTabStyle () {
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return { color: primaryColor }
    },
    getButtonStyle () {
      const accentColor = colorUtil.getEmployerAccentColor(this.employer)
      return {
        backgroundColor: accentColor,
        color: colorUtil.getInvertedColor(accentColor)
      }
    },
    getHeaderStyle () {
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return {
        backgroundColor: primaryColor,
        color: colorUtil.getInvertedColor(primaryColor)
      }
    },
    getSelectedCardStyle (job) {
      if (!this.jobApplication || this.jobApplication.id !== job.id) {
        return {}
      }
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return {
        boxShadow: `0 0 5px 2px ${primaryColor}`
      }
    },
    openJobAppModal (jobApplication) {
      return this.q.dialog({
        component: DialogJobApp,
        componentProps: { jobApplication, employer: this.employer },
        noRouteDismiss: true
      })
    }
  },
  async mounted () {
    if (!this.$route.meta.isExample) {
      await this.loadData()
    } else {
      Loading.show()
      await this.employerStore.setEmployer(this.$route.params.employerId)
      this.jobs = []
      this.employer = this.employerStore.getEmployer(this.$route.params.employerId)
      if (this.$route.params.ownerId) {
        await this.userStore.setUserProfile(this.$route.params.ownerId)
        this.profile = this.userStore.getUserProfile(this.$route.params.ownerId)
      } else {
        this.profile = null
      }
      Loading.hide()
    }

    await this.employerStore.setEmployerPage(this.employer.id)
    this.employerPage = this.employerStore.getEmployerPage(this.employer.id)

    const { jobId } = dataUtil.getQueryParams()
    if (jobId) {
      this.openApplication(null, parseInt(jobId))
    }

    this.isLoaded = true
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
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

    return {
      user,
      applications,
      isRightDrawerOpen,
      employerStore: useEmployerStore(),
      userStore: useUserStore(),
      q: useQuasar()
    }
  }
}
</script>

<style lang="scss" scoped>
.application-date {
  padding: 8px;
}
</style>
