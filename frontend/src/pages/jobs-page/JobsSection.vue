<template>
  <div class="row justify-center">
    <ResponsiveWidth>
      <div class="row">
        <div class="col-12 q-mb-md">
          <q-btn
            v-if="!isSingleJob"
            label="Filter jobs" color="primary" icon="filter_alt" class="q-mr-sm"
            @click="openJobFilter()"
          >
            <q-badge color="info" floating>{{ filterCount }}</q-badge>
          </q-btn>
          <q-btn v-if="hasBaseJobsPage() || (filterCount && !isSingleJob)" label="Show all jobs" color="grey-8" @click="goHome()"/>
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
          v-if="totalPageCount > 1"
          v-model="pageNumber"
          :max-pages="5"
          :max="totalPageCount"
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
                :user="user"
                :user-favorites="userFavorites"
                :jobs="jobs"
                :is-single-employer="isSingleEmployer"
                :is-jobs-closed="isJobsClosed"
                :job-application="job"
                :job-pages-count="totalPageCount"
                @openApplication="openApplication($event)"
                @updateApplications="loadJobs(true)"
                @updateUserFavorites="$emit('updateUserFavorites')"
              />
              <!--                TODO: Add recommendations button for mobile view-->
              <div
                v-if="false && !utilStore.isUnderBreakPoint('md')"
                class="col-3 q-py-md q-px-sm custom-sticky"
                style="align-self: start;"
              >
                <CollapsableCard
                  title="Recommendations"
                  :is-dense="true"
                >
                  <template v-slot:body>
                    <q-list class="w-100" dense style="max-height: 70vh; overflow-x: hidden; overflow-y: scroll">
<!--                      TODO: Add recommendations here - jobs, employers, professions -->
                    </q-list>
                  </template>
                </CollapsableCard>
              </div>
            </template>
          </div>
        </div>
        <q-pagination
          v-if="totalPageCount > 1"
          v-model="pageNumber"
          :max-pages="5"
          :max="totalPageCount"
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
import DialogJobFilter from 'components/dialogs/DialogJobFilter.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import ResponsiveWidth from 'components/ResponsiveWidth.vue'
import JobCards from 'pages/jobs-page/JobCards.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import scrollUtil from 'src/utils/scroll.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useSocialStore } from 'stores/social-store.js'
import { useUtilStore } from 'stores/utility-store.js'

const jobFiltersTemplate = {
  job_ids: [],
  location: null,
  range_miles: 50,
  search_regex: '',
  remote_type_bit: null,
  minimum_salary: null,
  job_profession_ids: []
}

const JOBS_PAGES = ['jobs-link', 'job', 'jobs', 'group', 'company', 'profession', 'profile']

export default {
  name: 'JobsSection',
  props: {
    user: [Object, null],
    employer: [Object, null],
    userFavorites: Object
  },
  components: {
    ResponsiveWidth, CollapsableCard, JobCards
  },
  data () {
    return {
      isLoaded: false,
      pageNumber: 1,
      jobFilters: {},
      jobs: [],
      totalEmployerJobCount: null,
      isJobsClosed: false,
      isSingleJob: false,
      totalPageCount: null,
      job: null,
      dataUtil,
      employerStyleUtil,
      scrollUtil,
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      socialStore: useSocialStore(),
      utilStore: useUtilStore(),
      q: useQuasar()
    }
  },
  computed: {
    isSingleEmployer () {
      return this.$route.name === 'company'
    },
    filterCount () {
      return Object.entries(this.jobFilters).reduce((filterCount, [filterKey, val]) => {
        if (['job_ids', 'search_regex', 'job_profession_ids'].includes(filterKey)) {
          if (val?.length) {
            filterCount++
          }
        } else if (!['range_miles', 'location_text'].includes(filterKey) && !dataUtil.isNil(val)) {
          filterCount++
        }
        return filterCount
      }, 0)
    }
  },
  watch: {
    pageNumber: {
      async handler () {
        await this.loadJobs()
      }
    },
    $route: {
      async handler () {
        const previousSub = dataUtil.getQueryParams().sub
        const hasFiltersChanged = await this.updateJobFilterFromQueryParams()
        const hasSubChanged = dataUtil.isDeepEqual(previousSub, dataUtil.getQueryParams().sub)
        if (JOBS_PAGES.includes(this.$route.name) && (hasFiltersChanged || hasSubChanged)) {
          await this.loadJobs()
        }
        await this.openApplication()
      }
    },
    user: {
      async handler () {
        await this.loadJobs(true)
      },
      deep: true
    }
  },
  methods: {
    hasBaseJobsPage () {
      return ('sub' in dataUtil.getQueryParams()) && ['company', 'group', 'profession'].includes(this.$route.name)
    },
    async goHome () {
      this.jobFilters = {}
      let deleteParams = null
      if (this.hasBaseJobsPage()) {
        deleteParams = ['sub']
      }
      const url = dataUtil.getUrlWithParams({ deleteParams })
      this.updateJobFilterQueryParams(url)
      await this.updateJobFilterFromQueryParams()
      await this.loadJobs()
    },
    getElementTop (elId) {
      const el = document.getElementById(elId)
      return el.getBoundingClientRect().top
    },
    openJobFilter () {
      return this.q.dialog({
        component: DialogJobFilter,
        componentProps: { jobFilters: this.jobFilters, isSingleEmployer: this.isSingleEmployer }
      }).onOk((newFilters) => {
        if (dataUtil.isDeepEqual(newFilters, this.jobFilters)) {
          return
        }
        this.jobFilters = newFilters
        if (this.pageNumber === 1) {
          this.loadJobs()
        } else {
          this.pageNumber = 1 // Changing the page number will load new jobs
        }
      })
    },
    openJobAppModal (jobApplication) {
      return this.q.dialog({
        component: DialogJobApp,
        componentProps: { jobApplication, employer: this.employer },
        noRouteDismiss: true
      })
    },
    async openApplication (jobId = null) {
      jobId = jobId || dataUtil.getQueryParams().jobId
      if (!jobId) {
        return
      }
      jobId = parseInt(jobId)

      await this.employerStore.setEmployerJobApplicationRequirements({ jobId })
      this.job = this.jobs.find((job) => job.id === jobId)
      this.job.application_fields = this.employerStore.getEmployerJobApplicationRequirements({ jobId })
      const fullPath = dataUtil.getUrlWithParams({
        addParams: [{ key: 'jobId', val: jobId }]
      })
      window.history.pushState({ path: fullPath }, '', fullPath)
      if (window.innerWidth < 600) {
        this.openJobAppModal(this.job).onDismiss(() => this.closeApplication())
      } else {
        this.$emit('openAppSideBar', this.job)
      }
      const jobElId = `job-${jobId}`
      scrollUtil.scrollTo(this.getElementTop(jobElId))
    },
    async closeApplication () {
      this.$emit('closeAppSideBar')
      this.job = null
      const fullPath = dataUtil.getUrlWithParams({
        deleteParams: ['jobId']
      })
      window.history.pushState({ path: fullPath }, '', fullPath)
    },
    async updateJobFilterFromQueryParams (isInit = false) {
      const previousParams = dataUtil.deepCopy(this.jobFilters)
      const params = dataUtil.getQueryParams()
      const intKeys = ['remote_type_bit', 'range_miles']
      const floatKeys = ['minimum_salary']
      const arrayKeys = ['job_ids', 'job_profession_ids']
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
      arrayKeys.forEach((key) => {
        if (params[key]) {
          params[key] = dataUtil.getForceArray(params[key]).map((val) => Number.parseInt(val))
        }
      })
      this.jobFilters = dataUtil.pick(params, Object.keys(jobFiltersTemplate))
      // Use the browser's country as an initial filter if a location is not already populated
      // Don't apply to groups since they have presumably already selected the appropriate geographies
      if (isInit && this.$route.name !== 'group') {
        params.location_text = params.location_text || this.$route.meta?.browserLocation?.country_name
      }
      if (params.location_text) {
        const resp = await this.$api.get('search/location/', {
          params: { search_text: params.location_text }
        })
        this.jobFilters.location = (resp.data?.length) ? resp.data[0] : null
      }
      return dataUtil.isDeepEqual(previousParams, this.jobFilters)
    },
    updateJobFilterQueryParams (startPath = null) {
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
        addParams, deleteParams: [...Object.keys(jobFiltersTemplate), 'location_text'], path: startPath
      })
      window.history.pushState({ path: fullPath }, '', fullPath)
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
    async loadJobs (isForceRefresh = false) {
      this.isLoaded = false
      const params = {
        linkId: this.$route.params.filterId,
        connectionId: this.$route.query.connect,
        employerKey: this.$route.params.employerKey,
        userKey: this.$route.params.userKey,
        isEmployer: this.$route.name === 'company',
        professionKey: this.$route.params.professionKey,
        jobKey: this.$route.params.jobKey,
        jobSubscriptionIds: dataUtil.getQueryParams().sub,
        pageNumber: this.pageNumber,
        jobFilters: this.jobFilters,
        isForceRefresh
      }

      await this.socialStore.setSocialLinkJobs(params)
      const {
        jobs,
        total_page_count: totalPageCount,
        total_job_count: totalEmployerJobCount,
        is_jobs_closed: isJobsClosed,
        is_single_job: isSingleJob
      } = this.socialStore.getSocialLinkJobs(params)

      this.totalEmployerJobCount = totalEmployerJobCount
      this.jobs = jobs || []
      this.totalPageCount = totalPageCount
      this.isJobsClosed = isJobsClosed
      this.isSingleJob = isSingleJob

      this.updateJobFilterQueryParams()
      this.isLoaded = true
      scrollUtil.scrollTo(0)
    }
  },
  async mounted () {
    await this.updateJobFilterFromQueryParams(true)
    await Promise.all([
      this.loadJobs()
    ])

    await this.openApplication()
  }
}
</script>
