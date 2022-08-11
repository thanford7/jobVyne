<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <FilterCard title="Jobs filter" class="q-mb-sm">
        <template v-slot:filters>
          <div class="col-12 col-md-4 q-pa-sm">
            <q-input filled borderless debounce="300" v-model="jobsFilter.jobTitle" placeholder="Job title">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
          </div>
          <div class="col-12 col-md-4 q-pa-sm">
            <SelectJobDepartment v-model="jobsFilter.departments"/>
          </div>
          <div class="col-12 col-md-4 q-pa-sm">
            <SelectJobCity v-model="jobsFilter.cities"/>
          </div>
          <div class="col-12 col-md-4 q-pa-sm">
            <SelectJobState v-model="jobsFilter.states"/>
          </div>
          <div class="col-12 col-md-4 q-pa-sm">
            <SelectJobCountry v-model="jobsFilter.countries"/>
          </div>
          <div class="col-12 col-md-4 q-pa-sm" style="font-size: 16px">
            <DateRangeSelector v-model="jobsFilter.dateRange" placeholder="Posted date"/>
          </div>
        </template>
      </FilterCard>
    </div>
    <div class="col-12">
      <q-table
        :rows="employerJobs"
        row-key="id"
        :columns="jobColumns"
        :filter-method="jobDataFilter"
        filter="jobsFilter"
        no-data-label="No jobs match the filter"
        :rows-per-page-options="[25, 50, 100]"
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
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import FilterCard from 'components/FilterCard.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

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
  } // TODO: Add referral bonus min/max
]

export default {
  name: 'JobsSection',
  components: { DateRangeSelector, SelectJobCountry, SelectJobState, SelectJobCity, SelectJobDepartment, FilterCard, CustomTooltip },
  data () {
    return {
      jobsFilter: {
        jobTitle: null,
        departments: null,
        cities: null,
        states: null,
        countries: null,
        dateRange: null
      },
      jobColumns
    }
  },
  computed: {
    employerJobs () {
      return this.employerStore.getEmployerJobs(this.user.employer_id)
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    jobDataFilter (jobs) {
      const departmentIds = (this.jobsFilter.departments) ? this.jobsFilter.departments.map((department) => department.id) : []
      const cityIds = (this.jobsFilter.cities) ? this.jobsFilter.cities.map((city) => city.id) : []
      const stateIds = (this.jobsFilter.states) ? this.jobsFilter.states.map((state) => state.id) : []
      const countryIds = (this.jobsFilter.countries) ? this.jobsFilter.countries.map((country) => country.id) : []
      const { from: fromDate, to: toDate } = this.jobsFilter.dateRange || {}
      return jobs.filter((job) => {
        const jobCityIds = job.locations.map((l) => l.city_id)
        const jobStateIds = job.locations.map((l) => l.state_id)
        const jobCountryIds = job.locations.map((l) => l.country_id)
        if (this.jobsFilter.jobTitle && this.jobsFilter.jobTitle.length) {
          const jobTitleRegex = new RegExp(`.*?${this.jobsFilter.jobTitle}.*?`, 'i')
          if (!job.job_title.match(jobTitleRegex)) {
            return false
          }
        }
        if (this.jobsFilter.departments?.length && !departmentIds.includes(job.job_department_id)) {
          return false
        }
        if (this.jobsFilter.cities?.length && !dataUtil.getArrayIntersection(cityIds, jobCityIds).length) {
          return false
        }
        if (this.jobsFilter.states?.length && !dataUtil.getArrayIntersection(stateIds, jobStateIds).length) {
          return false
        }
        if (this.jobsFilter.countries?.length && !dataUtil.getArrayIntersection(countryIds, jobCountryIds).length) {
          return false
        }
        if (fromDate && dateTimeUtil.isBefore(job.open_date, fromDate)) {
          return false
        }
        if (toDate && dateTimeUtil.isAfter(job.open_date, toDate)) {
          return false
        }
        return true
      })
    }
  },
  setup () {
    const employerStore = useEmployerStore()
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const q = useQuasar()

    return { employerStore, authStore, globalStore, q, user }
  }
}
</script>
