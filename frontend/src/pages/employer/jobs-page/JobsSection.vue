<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-table
        :rows="employerJobs"
        row-key="id"
        :columns="jobColumns"
        :filter-method="jobDataFilter"
        filter="jobsFilter"
        selection="multiple"
        v-model:selected="selectedJobs"
        no-data-label="No jobs match the filter"
        :rows-per-page-options="[25, 50, 100]"
      >
        <template v-slot:top>
          <CustomTooltip v-if="!selectedJobs.length" :is_include_icon="false" :is_include_space="true">
            <template v-slot:content>
              <q-btn
                unelevated
                :disable="true"
                label="Edit referral bonus" icon="edit" color="primary"
              />
            </template>
            Select at least one job to edit
          </CustomTooltip>
          <q-btn
            v-else
            unelevated
            label="Edit referral bonus" icon="edit" color="primary"
            @click="openEditJobBonusDialog"
          />
          <q-chip
            v-if="$route.query.ruleId"
            class="q-ml-md"
            removable
            @remove="removeRuleFilter"
          >
              <span v-if="parseInt($route.query.ruleId) > 0">
                Jobs matching&nbsp;
                <a
                  href="#"
                  @click="openShowBonusRuleDialog($event,$route.query.ruleId)"
                >referral bonus rule</a>
              </span>
            <span v-else>Jobs without matching bonus rule</span>
          </q-chip>
        </template>
        <template v-slot:header-cell-job_title="props">
          <q-th :props="props">
            {{ props.col.label }}
            <TableFilter filter-name="Job title" :has-filter="jobsFilter.jobTitle && jobsFilter.jobTitle.length">
              <q-input filled borderless debounce="300" v-model="jobsFilter.jobTitle" placeholder="Job title">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </q-th>
        </template>
        <template v-slot:header-cell-job_department="props">
          <q-th :props="props">
            {{ props.col.label }}
            <TableFilter filter-name="Job department"
                         :has-filter="jobsFilter.departments && jobsFilter.departments.length">
              <SelectJobDepartment v-model="jobsFilter.departments"/>
            </TableFilter>
          </q-th>
        </template>
        <template v-slot:header-cell-locations="props">
          <q-th :props="props">
            {{ props.col.label }}
            <TableFilter
              filter-name="Location"
              :has-filter="(
                (jobsFilter.cities && jobsFilter.cities.length) ||
                (jobsFilter.states && jobsFilter.states.length) ||
                (jobsFilter.countries && jobsFilter.countries.length)
              )"
            >
              <div class="q-gutter-y-sm">
                <SelectJobCity v-model="jobsFilter.cities"/>
                <SelectJobState v-model="jobsFilter.states"/>
                <SelectJobCountry v-model="jobsFilter.countries"/>
              </div>
            </TableFilter>
          </q-th>
        </template>
        <template v-slot:header-cell-open_date="props">
          <q-th :props="props">
            {{ props.col.label }}
            <TableFilter filter-name="Job department"
                         :has-filter="jobsFilter.dateRange">
              <DateRangeSelector v-model="jobsFilter.dateRange" placeholder="Posted date"/>
            </TableFilter>
          </q-th>
        </template>
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
        <template v-slot:body-cell-bonus="props">
          <q-td key="bonus" class="text-center">
            {{ dataUtil.formatCurrency(props.row.bonus.amount, { currency: props.row.bonus.currency.name }) }}
          </q-td>
        </template>
        <template v-slot:body-cell-bonus_rule="props">
          <q-td>
            <a
              v-if="!dataUtil.isEmpty(props.row.bonus_rule)"
              href="#" @click="openShowBonusRuleDialog($event, props.row.bonus_rule.id, props.row.bonus)"
            >Bonus rule</a>
            <span v-else-if="props.row.bonus.type === BONUS_TYPES.DEFAULT">Default</span>
            <span v-else>None</span>
          </q-td>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJobBonus from 'components/dialogs/DialogJobBonus.vue'
import DialogShowBonusRule from 'components/dialogs/DialogShowBonusRule.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import { BONUS_TYPES } from 'src/utils/bonus.js'
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
    sort: dateTimeUtil.sortDatesFn.bind(dateTimeUtil),
    format: dateTimeUtil.getShortDate.bind(dateTimeUtil)
  },
  {
    name: 'bonus',
    field: row => row.bonus.amount,
    align: 'center',
    label: 'Referral bonus',
    sortable: true,
    sort: (a, b) => parseInt(a) - parseInt(b)
  },
  { name: 'bonus_rule', field: 'bonus_rule', align: 'left', label: 'Bonus rule' }
]

export default {
  name: 'JobsSection',
  components: {
    DateRangeSelector,
    SelectJobCountry,
    SelectJobState,
    SelectJobCity,
    SelectJobDepartment,
    CustomTooltip,
    TableFilter
  },
  data () {
    return {
      dataUtil,
      BONUS_TYPES,
      jobsFilter: {
        jobTitle: null,
        departments: null,
        cities: null,
        states: null,
        countries: null,
        dateRange: null
      },
      jobColumns,
      selectedJobs: []
    }
  },
  computed: {
    employerJobs () {
      return this.employerStore.getEmployerJobs(this.user.employer_id)
    },
    employerBonusRules () {
      return this.employerStore.getEmployerBonusRules(this.user.employer_id)
    }
  },
  methods: {
    getFullLocation: locationUtil.getFullLocation,
    openEditJobBonusDialog () {
      return this.q.dialog({
        component: DialogJobBonus,
        componentProps: { jobs: this.selectedJobs }
      })
    },
    openShowBonusRuleDialog (e, bonusRuleId, bonus) {
      e.preventDefault()
      bonusRuleId = parseInt(bonusRuleId)
      const bonusRule = this.employerBonusRules.find((rule) => rule.id === bonusRuleId)
      return this.q.dialog({
        component: DialogShowBonusRule,
        componentProps: { bonusRule, bonus }
      })
    },
    removeRuleFilter () {
      this.$router.replace({ query: dataUtil.omit(this.$route.query, ['ruleId']) })
    },
    jobDataFilter (jobs) {
      const departmentIds = (this.jobsFilter.departments) ? this.jobsFilter.departments.map((department) => department.id) : []
      const cityIds = (this.jobsFilter.cities) ? this.jobsFilter.cities.map((city) => city.id) : []
      const stateIds = (this.jobsFilter.states) ? this.jobsFilter.states.map((state) => state.id) : []
      const countryIds = (this.jobsFilter.countries) ? this.jobsFilter.countries.map((country) => country.id) : []
      const ruleId = parseInt(this.$route.query.ruleId)
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
        if (ruleId > 0 && (!job.bonus_rule || job.bonus_rule.id !== ruleId)) {
          return false
        }
        // Filter for jobs without a bonus rule
        if (ruleId === -1 && job.bonus_rule) {
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
