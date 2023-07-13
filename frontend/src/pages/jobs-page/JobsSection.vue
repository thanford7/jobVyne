<template>
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
                      @keyup.enter="loadJobs()"
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
                      @update:location="loadJobs()"
                      @update:range_miles="loadJobs()"
                    />
                  </div>
                  <div class="col-12 col-md-4 q-pr-md-sm">
                    <SelectRemote v-model="jobFilters.remote_type_bit" @update:model-value="loadJobs()"/>
                  </div>
                  <div class="col-12 col-md-4 q-pl-md-sm">
                    <MoneyInput
                      v-model:money-value.number="jobFilters.minimum_salary"
                      v-model:currency-name="jobFilters.currency"
                      :is-include-currency-selection="false"
                      label="Minimum salary"
                      @submit="loadJobs()"
                    />
                  </div>
                  <div class="col-12">
                    <q-btn ref="filterSubmit" color="primary" label="Search" @click="loadJobs()"/>
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
            <template v-if="!isLoaded">
              <div class="col-12 col-md-9 q-mt-md q-gutter-y-sm">
                <q-skeleton type="rect" style="height: 15vh;"/>
                <q-skeleton type="rect" style="height: 15vh;"/>
                <q-skeleton type="rect" style="height: 15vh;"/>
              </div>
              <div v-if="!utilStore.isUnderBreakPoint('md')" class="col-3 q-py-md q-px-sm">
                <q-skeleton type="rect" style="height: 45vh;"/>
              </div>
            </template>
            <template v-else>
              <JobCards
                class="col-12 col-md-9 q-mt-md"
                :jobs-by-employer="jobsByEmployer"
                :is-single-employer="isSingleEmployer"
                :is-jobs-closed="isJobsClosed"
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
                    <q-list class="w-100" dense style="max-height: 70vh; overflow-x: hidden; overflow-y: scroll">
                      <template v-for="employer in jobsByEmployer">
                        <q-item
                          v-if="!isSingleEmployer"
                          clickable
                          class="text-bold"
                          @click="scrollUtil.scrollTo(getElementTop(`employer-${employer.employer_id}`))"
                        >
                          {{ employer.employer_name }}
                        </q-item>
                        <template v-for="(jobsByTitle, jobDepartment) in employer.jobs">
                          <q-item
                            v-if="$route.name !== 'profession'"
                            clickable
                            class="text-italic"
                            :style="(isSingleEmployer) ? '' : 'padding-left: 30px'"
                            @click="scrollUtil.scrollTo(getElementTop(`department-${employer.employer_id}-${dataUtil.removeStringSpecialChars(jobDepartment)}`))"
                          >
                            {{ jobDepartment }}
                          </q-item>
                          <q-item
                            v-for="(jobs, jobTitle) in jobsByTitle"
                            clickable
                            :style="(isSingleEmployer) ? 'padding-left: 30px' : 'padding-left: 45px'"
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
            </template>
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
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import DialogJobApp from 'components/dialogs/DialogJobApp.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import JobCards from 'pages/jobs-page/JobCards.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import scrollUtil from 'src/utils/scroll.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useSocialStore } from 'stores/social-store.js'
import { useUtilStore } from 'stores/utility-store.js'

const jobFiltersTemplate = {
  job_ids: [],
  location: null,
  range_miles: 50,
  search_regex: '',
  remote_type_bit: null,
  minimum_salary: null
}

export default {
  name: 'JobsSection',
  props: {
    user: [Object, null],
    employer: [Object, null],
    headerHeight: Number
  },
  components: {
    ResponsiveWidth, CollapsableCard, InputLocation, SelectRemote, MoneyInput, JobCards
  },
  data () {
    return {
      isLoaded: false,
      pageNumber: 1,
      jobFilters: {},
      jobsByEmployer: {},
      totalEmployerJobCount: null,
      isJobsClosed: false,
      jobPagesCount: null,
      applications: null,
      jobApplication: null,
      dataUtil,
      employerStyleUtil,
      scrollUtil,
      authStore: useAuthStore(),
      socialStore: useSocialStore(),
      utilStore: useUtilStore(),
      q: useQuasar()
    }
  },
  computed: {
    hasNoJobs () {
      return dataUtil.isEmpty(this.jobsByEmployer)
    },
    isSingleEmployer () {
      return this.jobsByEmployer.length === 1 && employerTypeUtil.isTypeEmployer(this.employer?.organization_type)
    }
  },
  watch: {
    pageNumber: {
      async handler () {
        await this.loadJobs()
      }
    },
    jobFilters: {
      handler () {
        // Reset page number if filters have changed
        this.pageNumber = 1
      },
      deep: true
    },
    $route: {
      async handler () {
        await this.updateJobFilterFromQueryParams()
        await this.loadJobs()
      },
      deep: true
    }
  },
  methods: {
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
    openJobAppModal (jobApplication) {
      return this.q.dialog({
        component: DialogJobApp,
        componentProps: { jobApplication, employer: this.employer },
        noRouteDismiss: true
      })
    },
    async openApplication (jobId) {
      this.jobApplication = this.getJobApplicationById(jobId)
      await this.$router.replace({ name: this.$route.name, query: Object.assign({}, this.$route.query, { jobId }) })
      if (window.innerWidth < 600) {
        this.openJobAppModal(this.jobApplication).onDismiss(() => this.closeApplication())
      } else {
        this.$emit('openAppSideBar')
      }
      scrollUtil.scrollToElement(document.getElementById(`job-${jobId}`))
    },
    async closeApplication () {
      this.$emit('closeAppSideBar')
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
    async updateJobFilterFromQueryParams () {
      const params = dataUtil.getQueryParams()
      const intKeys = ['remote_type_bit', 'range_miles']
      const floatKeys = ['minimum_salary']
      intKeys.forEach((key) => {
        if (params[key]) {
          params[key] = Number.parseInt(params[key])
        }
      })
      floatKeys.forEach((key) => {
        if (params[key]) {
          params[key] = Number.parseFloat(params[key])
        }
      })
      this.jobFilters = dataUtil.pick(params, Object.keys(jobFiltersTemplate))
      if (params.location_text) {
        const resp = await this.$api.get('search/location/', {
          params: { search_text: params.location_text }
        })
        this.jobFilters.location = (resp.data?.length) ? resp.data[0] : null
      }
    },
    updateJobFilterQueryParams () {
      const addParams = Object.entries(this.jobFilters).reduce((filterParams, [jobFilterKey, jobFilter]) => {
        if (!jobFilter) {
          return filterParams
        }
        if (jobFilterKey === 'location') {
          filterParams.push({
            key: 'location_text',
            val: jobFilter.text
          })
        } else {
          filterParams.push({
            key: jobFilterKey,
            val: jobFilter
          })
        }
        return filterParams
      }, [])
      const fullPath = dataUtil.getUrlWithParams({
        addParams, deleteParams: Object.keys(jobFiltersTemplate)
      })
      this.$router.push(fullPath)
    },
    resetJobFilters () {
      this.jobFilters = Object.assign({}, jobFiltersTemplate)
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
    async loadJobs () {
      this.isLoaded = false
      const params = {
        linkId: this.$route.params.filterId,
        employerKey: this.$route.params.employerKey,
        isEmployer: this.$route.name === 'company',
        professionKey: this.$route.params.professionKey,
        jobSubscriptionIds: dataUtil.getQueryParams().sub,
        pageNumber: this.pageNumber,
        jobFilters: this.jobFilters
      }

      await this.socialStore.setSocialLinkJobs(params)
      const {
        jobs_by_employer: jobsByEmployer,
        total_page_count: totalPageCount,
        total_employer_job_count: totalEmployerJobCount,
        is_jobs_closed: isJobsClosed
      } = this.socialStore.getSocialLinkJobs(params)

      this.totalEmployerJobCount = totalEmployerJobCount
      this.jobsByEmployer = jobsByEmployer || []
      this.jobPagesCount = totalPageCount
      this.isJobsClosed = isJobsClosed

      this.updateJobFilterQueryParams()
      this.isLoaded = true
    }
  },
  async mounted () {
    await this.updateJobFilterFromQueryParams()
    await Promise.all([
      this.loadJobs(),
      this.authStore.setApplications(this.user)
    ])
    const { applications } = storeToRefs(this.authStore)
    this.applications = applications
  }
}
</script>
