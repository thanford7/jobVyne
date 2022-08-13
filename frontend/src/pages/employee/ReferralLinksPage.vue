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
            <div class="col-12">
              <q-table
                :rows="socialStore.getOwnSocialLinkFilters()"
                :columns="linkColumns"
                row-key="id"
                :rows-per-page-options="[5, 10, 15]"
              >
                <template v-slot:top>
                  <q-btn ripple color="primary" label="Create new link" @click="tab = 'create'"/>
                </template>
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="platformName" :props="props">
                      {{ props.row.platform_name || globalStore.nullValueStr }}
                    </q-td>
                    <q-td key="departments" :props="props">
                      <q-chip
                        v-for="dept in props.row.departments"
                        :key="dept.id"
                        dense
                        color="blue-grey-7"
                        text-color="white"
                        size="13px"
                      >
                        {{ dept.name }}
                      </q-chip>
                      <span v-if="!props.row.departments.length">
                        {{ globalStore.nullValueAnyStr }}
                      </span>
                    </q-td>
                    <q-td key="departments" :props="props">
                      <q-chip
                        v-for="loc in getLocations(props.row)"
                        :key="loc.key"
                        dense
                        :color="loc.color"
                        text-color="white"
                        size="13px"
                      >
                        {{ loc.name }}
                      </q-chip>
                      <span v-if="!getLocations(props.row).length">
                        {{ globalStore.nullValueAnyStr }}
                      </span>
                    </q-td>
                    <q-td key="views" :props="props">
                      {{ props.row.performance.views.total }}
                    </q-td>
                    <q-td key="uniqueViews" :props="props">
                      {{ props.row.performance.views.unique }}
                    </q-td>
                    <q-td key="applications" :props="props">
                      <span v-if="props.row.performance.applications.length">
                        <a href="#" @click="selectedLinkId = props.row.id">
                          {{ props.row.performance.applications.length }}
                        </a>
                      </span>
                      <span v-else>
                        {{ props.row.performance.applications.length }}
                      </span>
                    </q-td>
                    <q-td key="link" :props="props">
                      <a :href="getJobLinkUrl(props.row)" target="_blank" class="no-decoration">
                        <span class="text-gray-3">
                          <q-icon name="launch"/>&nbsp;
                        </span>
                        {{ getJobLinkUrl(props.row) }}
                      </a>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>
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
                    (Optional) Select the platform where you will display the link
                  </h6>
                  <CustomTooltip>
                    Selecting a platform allows you to analyze the performance of each of your links based on each
                    platform
                  </CustomTooltip>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <q-select
                  filled
                  v-model="formData.platform"
                  :options="socialStore.platforms"
                  autocomplete="name"
                  option-value="name"
                  option-label="name"
                  label="Platform"
                >
                  <template v-slot:option="scope">
                    <q-item v-bind="scope.itemProps">
                      <q-item-section avatar>
                        <img :src="scope.opt.logo" alt="Logo" style="max-height: 20px">
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>{{ scope.opt.name }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="flex items-center">
                  <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
                    2
                  </div>
                  <h6 style="display: inline-block;">
                    (Optional) Add filters for the jobs to display when the link is clicked
                  </h6>
                  <CustomTooltip>
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
                  3
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
                        <CustomTooltip :is_include_space="false">
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
                  <span @click="copyText" style="cursor: pointer;">
                    <q-icon name="content_copy"></q-icon>
                    Click to copy
                  </span>
                </div>
                <div class="flex items-center">
                  <h6 class="font-secondary" style="display: inline-block;">
                    Suggested short link text: <span class="copy-target">{{ getJobLinkText(true) }}</span>&nbsp;
                  </h6>
                  <span @click="copyText" style="cursor: pointer;">
                    <q-icon name="content_copy"></q-icon>
                    Click to copy
                  </span>
                </div>
                <div class="flex items-center">
                  <h6 class="font-secondary" style="display: inline-block;">
                    Suggested link text: <span class="copy-target">{{ getJobLinkText(false) }}</span>&nbsp;
                  </h6>
                  <span @click="copyText" style="cursor: pointer;">
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
    name: 'referral_bonus',
    field: 'referral_bonus',
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
  platform: null,
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
      jobColumns
    }
  },
  computed: {
    linkColumns () {
      return [
        { name: 'platformName', field: 'platform_name', align: 'left', label: 'Platform', sortable: true },
        { name: 'departments', field: 'departments', align: 'left', label: 'Departments' },
        { name: 'locations', field: this.getLocations, align: 'left', label: 'Locations' },
        { name: 'views', field: 'performance.views.total', align: 'center', label: 'Views' },
        { name: 'uniqueViews', field: 'performance.views.unique', align: 'center', label: 'Unique views' },
        { name: 'applications', field: 'performance.applications', align: 'center', label: 'Applications' },
        { name: 'link', field: this.getJobLinkUrl, align: 'left', label: 'Link' }
      ]
    },
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
    copyText: dataUtil.copyText.bind(dataUtil),
    getFullLocation: locationUtil.getFullLocation,
    getLocations (row) {
      const locations = []
      dataUtil.getForceArray(row.cities).forEach((city) => {
        city.type = 'city'
        city.key = `city-${city.id}`
        city.color = 'blue-8'
        locations.push(city)
      })
      dataUtil.getForceArray(row.states).forEach((state) => {
        state.type = 'state'
        state.key = `state-${state.id}`
        state.color = 'teal-8'
        locations.push(state)
      })
      dataUtil.getForceArray(row.countries).forEach((country) => {
        country.type = 'country'
        country.key = `country-${country.id}`
        country.color = 'blue-grey-8'
        locations.push(country)
      })
      return locations
    },
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
    jobDataFilter (rows) {
      const departmentIds = (this.formData.departments) ? this.formData.departments.map((department) => department.id) : []
      const cityIds = (this.formData.cities) ? this.formData.cities.map((city) => city.id) : []
      const stateIds = (this.formData.states) ? this.formData.states.map((state) => state.id) : []
      const countryIds = (this.formData.countries) ? this.formData.countries.map((country) => country.id) : []
      return rows.filter((job) => {
        const jobCityIds = job.locations.map((l) => l.city_id)
        const jobStateIds = job.locations.map((l) => l.state_id)
        const jobCountryIds = job.locations.map((l) => l.country_id)
        if (this.formData.departments?.length && !departmentIds.includes(job.job_department_id)) {
          return false
        }
        if (this.formData.cities?.length && !dataUtil.getArrayIntersection(cityIds, jobCityIds).length) {
          return false
        }
        if (this.formData.states?.length && !dataUtil.getArrayIntersection(stateIds, jobStateIds).length) {
          return false
        }
        if (this.formData.countries?.length && !dataUtil.getArrayIntersection(countryIds, jobCountryIds).length) {
          return false
        }
        return true
      })
    },
    async saveLink () {
      const data = {
        owner_id: this.user.id,
        employer_id: this.user.employer_id,
        platform_id: this.formData?.platform?.id,
        department_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.departments?.map((dept) => dept.id)),
        cities: dataUtil.getArrayWithValuesOrNone(this.formData.cities),
        state_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.states?.map((state) => state.id)),
        country_ids: dataUtil.getArrayWithValuesOrNone(this.formData?.countries?.map((country) => country.id))
      }
      const resp = await this.$api.post('social-link-filter/', getAjaxFormData(data))
      this.linkId = resp.data.id
      this.socialStore.setSocialLinkFilters(true)
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
        socialStore.setSocialLinkFilters(),
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

    const pageTitle = 'Referral Links'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return { socialStore, employerStore, authStore, globalStore, utilStore, user }
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
