<template>
  <q-layout view="hHr lpR fFf">

    <q-header v-if="isLoaded" ref="header" elevated class="bg-white text-primary">
      <div class="justify-center row" style="position: relative">
        <q-toolbar class="col-12 col-md-11 col-lg-8 q-pt-md q-px-none justify-center">
          <q-toolbar-title shrink>
            <img v-if="employer?.logo_url" :src="employer.logo_url" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
            <img v-else src="~assets/jobVyneLogo.png" alt="Logo"
                 style="height: 40px; max-width: 120px; object-fit: scale-down">
          </q-toolbar-title>
        </q-toolbar>
        <div class="q-pt-md flex" style="position: absolute; top: 0; right: 10px;">
          <div class="q-mr-md clickable" :style="employerStyleUtil.getTabStyle(employer)" @click="openFeedbackModal()">
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
          <q-tabs align="center" v-model="tab" :style="employerStyleUtil.getTabStyle(employer)">
            <q-tab id="jv-tab-jobs" name="jobs" label="Jobs"/>
            <q-tab v-if="isShowEmployeeProfile" id="jv-tab-me" name="me"
                   :label="`About ${profile?.first_name}`"/>
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
      <q-page v-if="isLoaded">
        <q-tab-panels v-model="tab" animated keep-alive class="no-overflow">
          <q-tab-panel name="jobs" style="position: relative;">
            <div class="row justify-center">
              <ResponsiveWidth>
                <div class="row">
                  <div v-if="!user || dataUtil.isEmpty(user)" class="col-12 q-mb-md">
                    <q-card flat class="border-4-info">
                      <q-card-section class="text-center text-bold">
                        Want to track all your job applications?
                        <a href="#" @click.prevent="openLoginModal(false)">Login</a>
                        or <a href="#" @click.prevent="openLoginModal(true)">create an account</a>
                      </q-card-section>
                    </q-card>
                  </div>
                  <div class="col-12 q-mt-md">
                    <CollapsableCard title="Job filters" :is-dense="true">
                      <template v-slot:body>
                        <div class="col-12 q-pa-sm">
                          <q-form class="row q-gutter-y-sm">
                            <div class="col-12 col-md-4 q-pr-md-sm">
                              <q-input
                                v-model="jobFilters.search_regex"
                                filled
                                :label="(isSingleEmployer) ? 'Job title' : 'Job title or Company'"
                                debounce="500"
                                @keyup.enter="loadData()"
                              >
                                <template v-slot:append>
                                  <q-icon name="search"/>
                                </template>
                              </q-input>
                            </div>
                            <div class="col-12 col-md-8 q-pl-md-sm">
                              <InputLocation
                                v-model:location="jobFilters.location"
                                v-model:range_miles="jobFilters.range_miles"
                                :is-include-range="true"
                                @update:location="loadData()"
                                @update:range_miles="loadData()"
                              />
                            </div>
                            <div class="col-12 col-md-4 q-pr-md-sm">
                              <SelectRemote v-model="jobFilters.remote_type_bit" @update:model-value="loadData()"/>
                            </div>
                            <div class="col-12 col-md-4 q-pl-md-sm">
                              <MoneyInput
                                v-model:money-value="jobFilters.minimum_salary"
                                v-model:currency-name="jobFilters.currency"
                                :is-include-currency-selection="false"
                                label="Minimum salary"
                                @submit="loadData()"
                              />
                            </div>
                            <div class="col-12">
                              <q-btn ref="filterSubmit" color="primary" label="Search" @click="loadData()"/>
                            </div>
                          </q-form>
                        </div>
                      </template>
                    </CollapsableCard>
                  </div>
                  <div v-if="jobFilters?.job_ids?.length && totalEmployerJobCount > jobFilters.job_ids.length"
                       class="col-12 q-mt-md">
                    <q-btn
                      class="w-100" :label="`View all ${totalEmployerJobCount} jobs`"
                      icon="visibility" :style="employerStyleUtil.getButtonStyle(employer)"
                      @click="resetJobFilters"
                    />
                  </div>
                  <q-pagination
                    v-if="jobPagesCount > 1"
                    v-model="pageNumber"
                    :max-pages="5"
                    :max="jobPagesCount"
                    input
                    class="q-mt-md"
                  />
                  <div class="col-12 scroll" style="overflow: unset;">
                    <div class="row">
                      <JobCards
                        class="col-12 col-md-9 q-mt-md"
                        :employer="employer"
                        :jobs-by-employer="jobsByEmployer"
                        :is-single-employer="isSingleEmployer"
                        :has-no-jobs="hasNoJobs"
                        :applications="applications"
                        :job-application="jobApplication"
                        :job-pages-count="jobPagesCount"
                        :scroll-stick-start-px="headerHeight"
                        @openApplication="openApplication($event)"
                      />
                      <div
                        v-if="!utilStore.isUnderBreakPoint('md') && !hasNoJobs"
                        class="col-3 q-py-md q-px-sm custom-sticky"
                        style="align-self: start;"
                      >
                        <CollapsableCard
                          title="Job quick links"
                          :is-dense="true"
                        >
                          <template v-slot:body>
                            <q-list dense style="height: 25vh; overflow-x: hidden; overflow-y: scroll">
                              <template v-for="employer in jobsByEmployer">
                                <q-item
                                  v-if="!isSingleEmployer"
                                  clickable
                                  class="text-bold"
                                  @click="scrollUtil.scrollTo(getElementTop(`employer-${employer.employer_id}`))"
                                >
                                  {{ employer.employer_name }}
                                </q-item>
                                <template v-for="jobsByTitle in employer.jobs">
                                  <q-item
                                    v-for="(jobs, jobTitle) in jobsByTitle"
                                    clickable
                                    :style="(isSingleEmployer) ? '' : 'padding-left: 40px'"
                                    @click="scrollUtil.scrollTo(getElementTop(`job-${employer.employer_id}-${jobs[0].id}`))"
                                  >
                                    {{ jobTitle }}
                                  </q-item>
                                </template>
                              </template>
                            </q-list>
                          </template>
                        </CollapsableCard>
                      </div>
                    </div>
                  </div>
                  <q-pagination
                    v-if="jobPagesCount > 1"
                    v-model="pageNumber"
                    :max-pages="5"
                    :max="jobPagesCount"
                    input
                    class="q-mt-md"
                  />
                </div>
              </ResponsiveWidth>
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
        <q-page-scroller position="bottom-right" :scroll-offset="100" :offset="[40, 40]">
          <q-btn round color="primary" icon="arrow_upward"/>
        </q-page-scroller>
      </q-page>
    </q-page-container>

    <CustomFooter/>
  </q-layout>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import DialogFeedback from 'components/dialogs/DialogFeedback.vue'
import DialogJobApp from 'components/dialogs/DialogJobApp.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import FormJobApplication from 'components/job-app-form/FormJobApplication.vue'
import JobCards from 'pages/jobs-page/JobCards.vue'
import employerStyleUtil from 'src/utils/employer-styles.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import scrollUtil from 'src/utils/scroll.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import userUtil from 'src/utils/user.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useUserStore } from 'stores/user-store.js'
import { useUtilStore } from 'stores/utility-store.js'
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
  job_ids: [],
  location: null,
  range_miles: 50,
  search_regex: '',
  remote_type_bit: null,
  minimum_salary: null
}

export default {
  data () {
    return {
      tab: this.$route?.params?.tab || 'jobs',
      pageNumber: 1,
      totalEmployerJobCount: null,
      jobsByEmployer: null,
      employer: null,
      profile: null,
      isLoaded: false,
      jobApplication: null,
      jobPagesCount: null,
      jobFilters: {},
      headerHeight: 0,
      anchorPositions: {},
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      locationUtil,
      scrollUtil,
      userUtil
    }
  },
  components: {
    InputLocation,
    MoneyInput,
    ResponsiveWidth,
    CustomFooter,
    FormJobApplication,
    JobCards,
    CollapsableCard,
    SelectRemote
  },
  computed: {
    hasNoJobs () {
      return dataUtil.isEmpty(this.jobsByEmployer)
    },
    isSingleEmployer () {
      return this.jobsByEmployer.length === 1 && employerTypeUtil.isTypeEmployer(this.employer?.organization_type)
    },
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
        await this.loadData({ pageNumber: this.pageNumber })
      }
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    resetJobFilters () {
      this.jobFilters = Object.assign({}, jobFiltersTemplate)
    },
    async closeApplication () {
      this.isRightDrawerOpen = false
      this.jobApplication = null
      await this.$router.replace({
        name: this.$route.name,
        query: dataUtil.omit(this.$route.query || {}, ['jobId'])
      })
    },
    getJobApplicationById (jobId) {
      for (const employer of this.jobsByEmployer) {
        for (const jobPositions of Object.values(employer.jobs)) {
          for (const jobs of Object.values(jobPositions)) {
            for (const job of jobs) {
              if (job.id === jobId) {
                return job
              }
            }
          }
        }
      }
    },
    getElementTop (elId) {
      const el = document.getElementById(elId)

      // Sticky elements are outside of DOM flow and will cover up the top of the screen
      const scrollSticks = [
        document.querySelector('.custom-sticky-1'),
        document.querySelector('.custom-sticky-2'),
        document.querySelector('.custom-sticky-3')
      ].filter((s) => s)
      let stickHeight = 0
      scrollSticks.forEach((stick, idx) => {
        if (idx === scrollSticks.length - 1) {
          return
        }
        stickHeight += stick.offsetHeight
      })
      return el.getBoundingClientRect().top + window.scrollY - this.headerHeight - stickHeight
    },
    async openApplication (jobId) {
      this.jobApplication = this.getJobApplicationById(jobId)
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
    async loadData ({ isFirstLoad = false, pageNumber = 1 } = {}) {
      this.isLoaded = false
      Loading.show()
      const isExample = this.$route.meta.isExample
      let url = 'social-link-jobs/'
      if (this.$route.params.filterId) {
        url = `${url}${this.$route.params.filterId}`
      }
      const params = {
        page_count: pageNumber,
        employer_id: this.$route.params.employerId
      }
      // After the first page load, job filters are managed through the UI
      if (!isFirstLoad || isExample) {
        Object.assign(params, this.jobFilters)
      }
      const resp = await this.$api.get(url, { params })
      const {
        jobs_by_employer: jobsByEmployer,
        employer,
        total_page_count: totalPageCount,
        owner_id: ownerId,
        filter_values: filterValues,
        total_employer_job_count: totalEmployerJobCount
      } = resp.data

      if (isFirstLoad) {
        Object.assign(this.jobFilters, filterValues)
      }
      this.totalEmployerJobCount = totalEmployerJobCount
      if (!isExample) {
        await Promise.all([
          this.authStore.setApplications(this.user)
        ])
        if (ownerId) {
          await this.userStore.setUserProfile(ownerId)
        }
        this.profile = storeToRefs(this.userStore).userProfile
      } else {
        if (this.$route.params.ownerId) {
          await this.userStore.setUserProfile(this.$route.params.ownerId)
          this.profile = this.userStore.userProfile
        } else {
          this.profile = null
        }
      }
      this.jobsByEmployer = jobsByEmployer || []
      this.employer = employer

      this.jobPagesCount = totalPageCount
      this.isLoaded = true
      Loading.hide()
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
    },
    openLoginModal (isCreate) {
      return this.q.dialog({
        component: DialogLogin,
        componentProps: {
          isCreate,
          redirectPageUrl: window.location.pathname,
          redirectParams: dataUtil.getQueryParams(),
          userTypeBit: USER_TYPES[USER_TYPE_CANDIDATE],
          styleOverride: this.employerStyleUtil.getButtonStyle(this.employer)
        }
      })
    },
    setAnchorPositions () {
      this.jobsByEmployer.forEach((employer) => {
        const employerElId = `employer-${employer.employer_id}`
        this.anchorPositions[employerElId] = this.getElementTop(employerElId)
        employer.jobs.forEach((jobsByTitle) => {
          Object.entries(jobsByTitle).forEach(([jobs, jobTitle]) => {
            const jobElId = `job-${employer.employer_id}-${jobs[0].id}`
            this.anchorPositions[jobElId] = this.getElementTop(jobElId)
          })
        })
      })
    }
  },
  async mounted () {
    this.resetJobFilters()
    const params = Object.entries(dataUtil.getQueryParams()).reduce((params, [key, val]) => {
      params[key] = dataUtil.getForceArray(parseInt(val))
      return params
    }, {})
    Object.assign(this.jobFilters, params)
    await this.loadData({ isFirstLoad: true })

    const { jobId } = dataUtil.getQueryParams()
    if (jobId) {
      this.openApplication(parseInt(jobId))
    }
    this.headerHeight = this.$refs.header.$el.clientHeight
    // this.setAnchorPositions()
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
      utilStore: useUtilStore(),
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
