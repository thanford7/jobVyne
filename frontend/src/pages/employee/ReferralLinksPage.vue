<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Referral links">
        Add one or more referral links to your social media accounts. Anyone that visits your page can click on the
        link
        and will be directed to a webpage with all open jobs at your company. If they apply and work at your company,
        you can collect a referral bonus!
      </PageHeader>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="current" label="Current links"/>
        <q-tab name="create" label="Create link"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="current">
          <div class="row">
            <div
              v-for="socialLinkFilter in socialStore.getSocialLinkFilters(authStore.propUser.id)"
              class="col-12 col-md-4 q-pa-sm"
            >
              <q-card class="h-100">
                <div class="row q-pt-sm q-px-xs border-bottom-1-gray-500">
                  <q-chip
                    v-for="dept in socialLinkFilter.departments"
                    dense color="blue-grey-7" text-color="white" size="13px"
                  >
                    {{ dept.name }}
                  </q-chip>
                  <q-chip v-if="!socialLinkFilter.departments.length" dense size="13px">
                    Any department
                  </q-chip>
                  <q-chip
                    v-for="loc in getLocations(socialLinkFilter)"
                    dense :color="loc.color" text-color="white" size="13px"
                  >
                    {{ loc.name }}
                  </q-chip>
                  <q-chip v-if="!getLocations(socialLinkFilter).length" dense size="13px">
                    Any location
                  </q-chip>
                  <q-space/>
                  <a
                    :href="getJobLinkUrl(socialLinkFilter)"
                    target="_blank"
                    class="no-decoration"
                  >
                      <span class="text-gray-3" title="View jobs page">
                        <q-icon name="launch" size="24px"/>&nbsp;
                      </span>
                  </a>
                </div>
                <div class="q-px-md q-pb-sm">
                  <div>
                    <div class="q-mb-sm">
                      <span class="text-bold">Social Links</span> <span class="text-small">(Click to copy)</span>
                    </div>
                    <div v-for="socialLink in getSocialLinks(socialLinkFilter)" style="display: inline-block">
                      <q-chip clickable @click="dataUtil.copyText">
                        <div class="flex items-center">
                          <img :src="socialLink.logo" :alt="socialLink.name" style="height: 16px;">
                          <span class="copy-target" style="display: none;">{{ socialLink.socialLink }}</span>
                        </div>
                      </q-chip>
                    </div>
                  </div>
                  <div>
                    <div class="text-bold">Performance</div>
                    <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                      <div>{{ socialLinkFilter.performance.views.total }}</div>
                      <div class="text-small">Total views</div>
                    </div>
                    <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                      <div>{{ socialLinkFilter.performance.views.unique }}</div>
                      <div class="text-small">Unique views</div>
                    </div>
                    <div class="q-mx-sm q-my-xs" style="display: inline-block;">
                      <div>
                      <span v-if="socialLinkFilter.performance.applications.length">
                        <a href="#" @click.prevent="selectedLinkId = socialLinkFilter.id">
                          {{ socialLinkFilter.performance.applications.length }}
                        </a>
                      </span>
                        <span v-else>
                        {{ socialLinkFilter.performance.applications.length }}
                      </span>
                      </div>
                      <div class="text-small">Applications</div>
                    </div>
                  </div>
                </div>
              </q-card>
            </div>
            <div v-if="selectedLinkFilter" class="col-12 q-mt-md">
              <q-table
                :rows="jobLinkApplications"
                :columns="applicationsColumns"
                row-key="id"
                :rows-per-page-options="[5, 10, 15]"
                style="position: relative"
              >
                <template v-slot:top>
                  <div class="q-table__title">Job applications</div>
                  <q-space/>
                  <q-btn
                    flat unelevated ripple
                    icon="close"
                    text-color="grey-7"
                    size="md"
                    class="q-pr-sm"
                    style="position: absolute; top: 0; right: 0;"
                    @click="selectedLinkId = null"
                  />
                </template>
              </q-table>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="create">
          <div v-if="!linkId">
            <div class="row">
              <div class="col-12">
                <div class="flex items-center">
                  <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
                    1
                  </div>
                  <h6 style="display: inline-block;">
                    (Optional) Add filters for the jobs to display when the link is clicked
                  </h6>
                  <CustomTooltip :is_include_space="true">
                    Leave blank if you wish to display all jobs. Keep in mind that your link will perform better if the
                    filtered jobs are relevant to your connections/audience
                  </CustomTooltip>
                </div>
              </div>
              <div class="col-12">
                <div class="row">
                  <div class="col-12 col-md-6 q-pr-md-sm">
                    <SelectJobDepartment v-model="formData.departments"/>
                  </div>
                  <div class="col-12 col-md-6">
                    <SelectJobCity v-model="formData.cities"/>
                  </div>
                  <div class="col-12 col-md-6 q-pr-md-sm">
                    <SelectJobState v-model="formData.states"/>
                  </div>
                  <div class="col-12 col-md-6">
                    <SelectJobCountry v-model="formData.countries"/>
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
                  2
                </div>
                <h6 style="display: inline-block;">These are the currently open jobs based on the filter</h6>
              </div>
              <div class="col-12">
                <q-table
                  :rows="employerStore.getEmployerJobs(user.employer_id)"
                  row-key="id"
                  :columns="jobColumns"
                  :filter-method="jobDataFilter"
                  filter="formData"
                  no-data-label="No jobs match the filter"
                  :rows-per-page-options="[5, 10, 15]"
                >
                  <template v-slot:body-cell-locations="props">
                    <q-td>
                      <template v-if="props.row.locations.length > 1">
                        <CustomTooltip>
                          <template v-slot:icon>
                            <q-chip
                              color="grey-7" text-color="white" size="13px" dense
                            >
                              Multiple locations
                            </q-chip>
                          </template>
                          <ul>
                            <li v-for="location in props.row.locations">
                              {{ getFullLocation(location) }}
                            </li>
                          </ul>
                        </CustomTooltip>
                      </template>
                      <q-chip
                        v-else-if="props.row.locations.length"
                        dense
                        color="grey-7"
                        text-color="white"
                        size="13px"
                      >
                        {{ getFullLocation(props.row.locations[0]) }}
                      </q-chip>
                    </q-td>
                  </template>
                  <template v-slot:body-cell-referral_bonus="props">
                    <q-td key="bonus" class="text-center">
                      {{ dataUtil.formatCurrency(props.row.bonus.amount, { currency: props.row.bonus.currency.name }) }}
                    </q-td>
                  </template>
                </q-table>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <q-btn ripple color="primary" label="Generate link" size="lg" @click="saveLink"/>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="row">
              <div class="col-12">
                <div class="flex items-center">
                  <h6 class="font-secondary" style="display: inline-block;">
                    Link: <span class="copy-target">{{ getJobLinkUrl() }}</span>&nbsp;
                  </h6>
                  <span @click="dataUtil.copyText" style="cursor: pointer;">
                    <q-icon name="content_copy"></q-icon>
                    Click to copy
                  </span>
                </div>
                <div class="flex items-center">
                  <h6 class="font-secondary" style="display: inline-block;">
                    Suggested short link text: <span class="copy-target">{{ getJobLinkText(true) }}</span>&nbsp;
                  </h6>
                  <span @click="dataUtil.copyText" style="cursor: pointer;">
                    <q-icon name="content_copy"></q-icon>
                    Click to copy
                  </span>
                </div>
                <div class="flex items-center">
                  <h6 class="font-secondary" style="display: inline-block;">
                    Suggested link text: <span class="copy-target">{{ getJobLinkText(false) }}</span>&nbsp;
                  </h6>
                  <span @click="dataUtil.copyText" style="cursor: pointer;">
                    <q-icon name="content_copy"></q-icon>
                    Click to copy
                  </span>
                </div>
                <div class="q-mt-md">
                  <q-btn ripple color="primary" label="Create another link" @click="resetLinkForm()"/>
                </div>
              </div>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import jobsUtil from 'src/utils/jobs.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests'
import { useAuthStore } from 'stores/auth-store'
import { useEmployerStore } from 'stores/employer-store'
import { useSocialStore } from 'stores/social-store'
import { useUtilStore } from 'stores/utility-store'
import dataUtil from 'src/utils/data'
import dateTimeUtil from 'src/utils/datetime'
import CustomTooltip from 'components/CustomTooltip.vue'
import { useGlobalStore } from 'stores/global-store'
import { Loading, useMeta } from 'quasar'
import PageHeader from 'components/PageHeader.vue'

const jobColumns = [
  { name: 'job_title', field: 'job_title', align: 'left', label: 'Title', sortable: true },
  { name: 'job_department', field: 'job_department', align: 'left', label: 'Department', sortable: true },
  { name: 'locations', field: 'locations', align: 'left', label: 'Location' },
  {
    name: 'open_date',
    field: 'open_date',
    align: 'left',
    label: 'Posted Date',
    sortable: true,
    format: dateTimeUtil.getShortDate.bind(dateTimeUtil)
  },
  {
    name: 'bonus',
    field: row => row.bonus.amount,
    label: 'Referral Bonus',
    sortable: true,
    sort: (a, b) => parseInt(a) - parseInt(b),
    format: dataUtil.formatCurrency
  }
]

const applicationsColumns = [
  { name: 'first_name', field: 'first_name', align: 'left', label: 'First name', sortable: true },
  { name: 'last_name', field: 'last_name', align: 'left', label: 'Last name', sortable: true },
  { name: 'job_title', field: 'job_title', align: 'left', label: 'Job title', sortable: true },
  {
    name: 'apply_dt',
    field: 'apply_dt',
    align: 'left',
    label: 'Application date',
    sortable: true,
    format: dateTimeUtil.getShortDate.bind(dateTimeUtil)
  }
]

const formDataTemplate = {
  departments: null,
  cities: null,
  states: null,
  countries: null
}

export default {
  components: { SelectJobCountry, SelectJobState, SelectJobCity, SelectJobDepartment, PageHeader, CustomTooltip },
  data () {
    return {
      formData: { ...formDataTemplate },
      linkId: null,
      selectedLinkId: null, // Used to drill into application details
      tab: 'current',
      applicationsColumns,
      jobColumns,
      dataUtil
    }
  },
  computed: {
    selectedLinkFilter () {
      return dataUtil.getForceArray(this.socialStore.socialLinkFilters).find((linkFilter) => linkFilter.id === this.selectedLinkId)
    },
    jobLinkApplications () {
      if (!this.selectedLinkFilter) {
        return null
      }
      const applications = this.selectedLinkFilter.performance.applications
      return (applications.length) ? applications : null
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    getLocations: locationUtil.getFormattedLocations.bind(locationUtil),
    getJobLinkUrl (jobLink) {
      const id = (jobLink) ? jobLink.id : this.linkId
      return `${window.location.origin}/jobs-link/${id}`
    },
    getJobLinkName (defaultName = null, { departments, cities, states, countries }) {
      let jobLinkName = ''
      if (departments) {
        const deptString = (departments.length > 1) ? 'departments' : 'department'
        jobLinkName += ' in the ' + dataUtil.concatWithAnd(departments.map((d) => d.name)) + ' ' + deptString
      }
      if (cities && cities.length) {
        jobLinkName += ' in ' + dataUtil.concatWithAnd(this.formData.cities)
      } else if (states && states.length) {
        jobLinkName += ' in ' + dataUtil.concatWithAnd(this.formData.states.map((s) => s.state))
      } else if (countries && countries.length) {
        jobLinkName += ' in ' + dataUtil.concatWithAnd(this.formData.countries.map((c) => c.country))
      }
      return (defaultName && !jobLinkName.length) ? defaultName : jobLinkName
    },
    getJobLinkText (isShort) {
      const employer = this.employerStore.getEmployer(this.user.employer_id)
      if (!employer) {
        return ''
      }
      if (isShort) {
        return `${employer.name} is hiring! Apply ->`
      }
      let text = `${employer.name} is hiring! Click to apply`
      const jobText = this.getJobLinkName(null, this.formData)

      if (jobText.length) {
        text += ' to jobs' + jobText
      }

      text += '!'
      return text
    },
    getSocialLinks (jobLink) {
      return this.platforms.reduce((socialLinks, platform) => {
        const socialLink = dataUtil.getUrlWithParams({
          isExcludeExistingParams: true,
          path: this.getJobLinkUrl(jobLink),
          addParams: [{ key: 'platform', val: platform.name }]
        })
        socialLinks.push(Object.assign(
          dataUtil.pick(platform, ['name', 'logo']),
          { socialLink }
        ))
        return socialLinks
      }, [])
    },
    jobDataFilter (rows) {
      return jobsUtil.filterJobs(this.formData, rows)
    },
    async saveLink () {
      const data = {
        owner_id: this.user.id,
        employer_id: this.user.employer_id,
        department_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.departments?.map((dept) => dept.id)),
        city_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.cities?.map((city) => city.id)),
        state_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.states?.map((state) => state.id)),
        country_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.countries?.map((country) => country.id))
      }
      const resp = await this.$api.post('social-link-filter/', getAjaxFormData(data))
      this.linkId = resp.data.id
      await this.socialStore.setSocialLinkFilters(this.user.id, true)
    },
    resetLinkForm () {
      this.formData = { ...formDataTemplate }
      this.linkId = null
    }
  },
  preFetch () {
    const socialStore = useSocialStore()
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        socialStore.setPlatforms(),
        socialStore.setSocialLinkFilters(authStore.propUser.id),
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerJobs(authStore.propUser.employer_id)
      ])
    }).finally(() => Loading.hide())
  },
  setup () {
    const socialStore = useSocialStore()
    const employerStore = useEmployerStore()
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const utilStore = useUtilStore()
    const { user } = storeToRefs(authStore)
    const { platforms } = storeToRefs(socialStore)

    const pageTitle = 'Referral Links'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return { socialStore, employerStore, authStore, globalStore, utilStore, platforms, user }
  }
}
</script>

<style lang="scss" scoped>
.row {
  margin-bottom: 8px;
}

.col-12 {
  margin-bottom: 8px;
}
</style>
