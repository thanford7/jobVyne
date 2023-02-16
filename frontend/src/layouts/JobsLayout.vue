<template>
  <q-layout view="hHr lpR fFf">

    <q-header v-if="isLoaded" elevated class="bg-white text-primary">
      <div class="justify-center row" style="position: relative">
        <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
          <q-toolbar-title shrink>
            <img :src="employer?.logo_url" alt="Logo" style="height: 40px; object-fit: scale-down">
          </q-toolbar-title>
        </q-toolbar>
        <div class="q-pt-md flex" style="position: absolute; top: 0; right: 10px;">
          <div class="q-mr-md clickable" :style="getTabStyle()" @click="openFeedbackModal()">
            <div class="flex flex-center">
              <q-icon name="feedback" size="24px"/>
            </div>
            <div>Get help</div>
          </div>
          <div v-if="user && !dataUtil.isEmpty(user)">
            <div class="row flex-center">
              <q-avatar v-if="user.profile_picture_url" size="24px">
                <img :src="user.profile_picture_url">
              </q-avatar>
              <q-avatar v-else color="primary" text-color="white" size="24px">
                {{ userUtil.getUserInitials(user) }}
              </q-avatar>
            </div>
            <div>
              <a href="#" @click.prevent="logoutUser()" id="jv-logout" style="color: gray">Logout</a>
            </div>
          </div>
        </div>
        <ResponsiveWidth class="justify-center">
          <q-tabs align="center" v-model="tab" :style="getTabStyle()">
            <q-tab id="jv-tab-jobs" name="jobs" label="Jobs"/>
            <q-tab v-if="employerPage && employerPage.is_viewable" id="jv-tab-company" name="company"
                   :label="`About ${employer?.name}`"/>
            <q-tab v-if="isShowEmployeeProfile" id="jv-tab-me" name="me" :label="`About ${profile?.first_name}`"/>
          </q-tabs>
        </ResponsiveWidth>
      </div>
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
        ref="jobApplicationForm"
        :job-application="jobApplication"
        :employer="employer"
        @login="loadData()"
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

    <q-page-container class="q-pt-none">
      <q-page v-if="isLoaded" class="scroll">
        <q-tab-panels v-model="tab" animated keep-alive>
          <q-tab-panel name="jobs">
            <div class="row justify-center">
              <ResponsiveWidth>
                <q-page padding>
                  <div v-if="isActiveEmployer && isActiveEmployee" class="row">
                    <div class="col-12">
                      <CollapsableCard title="Job filters" :is-dense="true">
                        <template v-slot:body>
                          <div class="col-12 q-pa-sm">
                            <div class="row q-gutter-y-sm">
                              <div class="col-12 col-md-6 q-pr-md-sm">
                                <q-input
                                  v-model="jobFilters.job_title"
                                  filled label="Job title"
                                />
                              </div>
                              <div class="col-12 col-md-6 q-pl-md-sm">
                                <SelectJobDepartment
                                  v-if="employer?.id"
                                  v-model="jobFilters.department_ids"
                                  :employer-id="employer.id"
                                  :is-emit-id="true"
                                />
                              </div>
                              <div class="col-12 col-md-4 q-pr-md-sm">
                                <SelectJobCity
                                  v-if="employer?.id"
                                  v-model="jobFilters.city_ids"
                                  :employer-id="employer.id"
                                  :is-emit-id="true"
                                />
                              </div>
                              <div class="col-12 col-md-4 q-px-md-sm">
                                <SelectJobState
                                  v-if="employer?.id"
                                  v-model="jobFilters.state_ids"
                                  :employer-id="employer.id"
                                  :is-emit-id="true"
                                />
                              </div>
                              <div class="col-12 col-md-4 q-pl-md-sm">
                                <SelectJobCountry
                                  v-if="employer?.id"
                                  v-model="jobFilters.country_ids"
                                  :employer-id="employer.id"
                                  :is-emit-id="true"
                                />
                              </div>
                            </div>
                          </div>
                        </template>
                      </CollapsableCard>
                    </div>
                    <div v-if="jobFilters?.job_ids?.length && totalEmployerJobCount > jobFilters.job_ids.length"
                         class="col-12 q-mt-md">
                      <q-btn
                        class="w-100" :label="`View all ${totalEmployerJobCount} jobs`"
                        icon="visibility" :style="getButtonStyle()"
                        @click="resetJobFilters"
                      />
                    </div>
                    <div class="col-12 q-mt-lg">
                      <div v-if="!jobs.length" class="q-mb-md">
                        <q-card class="q-pa-lg">
                          <div class="text-h6 text-center">No current job openings</div>
                        </q-card>
                      </div>
                      <div v-for="job in jobs" :key="job.id" class="q-mb-md">
                        <q-card :style="getSelectedCardStyle(job)" :id="`job-${job.id}`" class="jv-job-card">
                          <div v-if="getJobApplication(job.id)" class="application-date" :style="getHeaderStyle()">
                            Applied on {{ dateTimeUtil.getShortDate(getJobApplication(job.id).created_dt) }}
                          </div>
                          <q-card-section class="q-pb-none">
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
                            <div
                              :id="`job-description-${job.id}`"
                              class="q-px-sm q-pt-sm"
                              :style="(job.isShowFullDescription) ? '' : 'max-height: 300px; overflow: hidden;'"
                              v-html="formUtil.sanitizeHtml(job.job_description)"
                            ></div>
                            <template
                              v-if="job.hasDescriptionOverflow || hasJobDescriptionOverflow(job) || !dataUtil.isNil(job.isShowFullDescription)">
                              <div v-if="!job.isShowFullDescription" class="q-py-md">
                                <a
                                  href="#" @click.prevent="job.isShowFullDescription = true"
                                >
                                  Show full job description
                                </a>
                              </div>
                              <div v-else>
                                <a
                                  href="#" @click.prevent="job.isShowFullDescription = false"
                                >
                                  Reduce job description
                                </a>
                              </div>
                            </template>
                          </q-card-section>
                          <q-separator dark/>
                          <q-card-actions v-if="!getJobApplication(job.id)">
                            <q-btn
                              ripple unelevated
                              class="jv-apply-btn"
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
                            <span v-if="!isActiveEmployer">
                              {{ employer.name }} no longer has an active JobVyne account. If you wish to
                              view and apply for jobs, please visit their
                            </span>
                            <span v-else>
                              {{ profile.first_name }} {{
                                profile.last_name
                              }} does not have an active account with {{ employer.name }}. If
                              you wish to view and apply for jobs, please visit {{ employer.name }}'s
                            </span>
                            <a v-if="employer.company_jobs_page_url" :href="employer.company_jobs_page_url"
                               target="_blank" class="text-white">
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
              <div class="col-12 col-md-3 q-pr-md-md q-mb-md q-mb-md-none">
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
              <div class="col-12 col-md-4 q-pl-md-md">
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
import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogFeedback from 'components/dialogs/DialogFeedback.vue'
import DialogJobApp from 'components/dialogs/DialogJobApp.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import EmployerProfile from 'pages/jobs-page/EmployerProfile.vue'
import colorUtil from 'src/utils/color.js'
import formUtil from 'src/utils/form.js'
import scrollUtil from 'src/utils/scroll.js'
import userUtil from 'src/utils/user.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useUserStore } from 'stores/user-store.js'
import { ref } from 'vue'
import CustomFooter from 'components/CustomFooter.vue'
import locationUtil from 'src/utils/location'
import dataUtil from 'src/utils/data'
import { useAuthStore } from 'stores/auth-store'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useGlobalStore } from 'stores/global-store'
import dateTimeUtil from 'src/utils/datetime'
import { storeToRefs } from 'pinia/dist/pinia'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'

const jobFiltersTemplate = {
  department_ids: [],
  city_ids: [],
  state_ids: [],
  country_ids: [],
  job_ids: [],
  job_title: ''
}

export default {
  data () {
    return {
      tab: this.$route?.params?.tab || 'jobs',
      jobDescriptionCharacterLimit: 1000,
      totalEmployerJobCount: null,
      jobs: null,
      employer: null,
      employerPage: null,
      profile: null,
      isLoaded: false,
      isActiveEmployer: null,
      isActiveEmployee: null,
      jobApplication: null,
      jobPagesCount: null,
      pageNumber: 1,
      jobFilters: {},
      dataUtil,
      dateTimeUtil,
      formUtil,
      locationUtil,
      userUtil
    }
  },
  components: {
    CustomTooltip,
    EmployerProfile,
    ResponsiveWidth,
    CustomFooter,
    FormJobApplication,
    CollapsableCard,
    SelectJobDepartment,
    SelectJobCity,
    SelectJobState,
    SelectJobCountry
  },
  computed: {
    employmentYears () {
      if (!this.profile.employment_start_date) {
        return null
      }
      return dateTimeUtil.getDateDifference(this.profile.employment_start_date, dateTimeUtil.now(), 'years')
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
    },
    jobFilters: {
      async handler () {
        await this.loadData({ isShowLoading: false })
      },
      deep: true
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getSalaryRange: dataUtil.getSalaryRange.bind(dataUtil),
    resetJobFilters () {
      this.jobFilters = Object.assign({}, jobFiltersTemplate)
    },
    hasJobDescriptionOverflow (job) {
      const el = document.getElementById(`job-description-${job.id}`)
      if (!el) {
        return false
      }
      job.hasDescriptionOverflow = scrollUtil.getHasOverflow(el)
      return job.hasDescriptionOverflow
    },
    async closeApplication () {
      this.isRightDrawerOpen = false
      this.jobApplication = null
      await this.$router.replace({
        name: this.$route.name,
        query: dataUtil.omit(this.$route.query || {}, ['jobId'])
      })
    },
    async openApplication (e, jobId) {
      this.jobApplication = this.jobs.find((j) => j.id === jobId)
      await this.$router.replace({ name: this.$route.name, query: Object.assign({}, this.$route.query, { jobId }) })
      if (window.innerWidth < 600) {
        this.openJobAppModal(this.jobApplication).onDismiss(() => this.closeApplication())
      } else {
        this.isRightDrawerOpen = true
      }
      scrollUtil.scrollToElement(document.getElementById(`job-${jobId}`))
    },
    async logoutUser () {
      await this.authStore.logout(false)
      await this.loadData()
    },
    async loadData ({ isShowLoading = true, isFirstLoad = false } = {}) {
      if (isShowLoading) {
        Loading.show()
      }
      let url = 'social-link-jobs/'
      if (this.$route.params.filterId) {
        url = `${url}${this.$route.params.filterId}`
      }
      const params = {
        page_count: this.pageNumber,
        employer_id: this.$route.params.employerId
      }
      // After the first page load, job filters are managed through the UI
      if (!isFirstLoad) {
        Object.assign(params, this.jobFilters)
      }
      const resp = await this.$api.get(url, { params })
      const {
        jobs,
        employer,
        total_page_count: totalPageCount,
        owner_id: ownerId,
        is_active_employee: isActiveEmployee,
        filter_values: filterValues,
        total_employer_job_count: totalEmployerJobCount
      } = resp.data

      if (isFirstLoad) {
        Object.assign(this.jobFilters, filterValues)
      }
      this.totalEmployerJobCount = totalEmployerJobCount
      if (!this.$route.meta.isExample) {
        await Promise.all([
          this.employerStore.setEmployerSubscription(employer.id),
          this.authStore.setApplications(this.user),
          this.userStore.setUserProfile(ownerId)
        ])
        const { is_active: isActiveEmployer } = this.employerStore.getEmployerSubscription(employer.id)
        this.isActiveEmployer = isActiveEmployer
        this.isActiveEmployee = isActiveEmployee
        this.profile = storeToRefs(this.userStore).userProfile
      } else {
        this.isActiveEmployer = true
        this.isActiveEmployee = true
        if (this.$route.params.ownerId) {
          await this.userStore.setUserProfile(this.$route.params.ownerId)
          this.profile = this.userStore.userProfile
        } else {
          this.profile = null
        }
      }
      this.jobs = (this.isActiveEmployer && this.isActiveEmployee) ? jobs : []
      this.employer = employer

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
    },
    openFeedbackModal () {
      return this.q.dialog({
        component: DialogFeedback
      })
    }
  },
  async mounted () {
    this.resetJobFilters()
    await this.loadData({ isFirstLoad: true })
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

    useMeta(globalStore.getMetaCfg({
      pageTitle: 'Jobs',
      description: 'Apply to jobs on JobVyne'
    }))

    return {
      user,
      applications,
      isRightDrawerOpen,
      authStore,
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
