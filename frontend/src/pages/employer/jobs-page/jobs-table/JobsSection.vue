<template>
  <div class="row q-gutter-y-md">
    <div class="col-12">
      <q-table
        :loading="isLoading"
        :rows="employerJobs"
        row-key="id"
        :columns="jobColumns"
        :filter-method="jobDataFilter"
        filter="jobsFilter"
        no-data-label="No jobs match the filter"
        :rows-per-page-options="[25, 50, 100]"
      >
        <template v-if="isEmployer" v-slot:top>
          <div class="col-12">
            <div class="row q-gutter-sm">
              <q-btn
                v-if="employer?.is_manual_job_entry"
                unelevated label="Add job" icon="add" color="primary"
                @click.prevent="openEditJobDialog()"
              />
              <q-btn
                v-if="employer?.ats_cfg?.id"
                unelevated label="Update jobs from ATS" icon="refresh" color="primary"
                :loading="isFetchingJobs"
                @click.prevent="updateAtsJobs()"
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
              <q-space/>
              <q-btn-toggle
                v-model="isClosedJobs"
                unelevated
                class="border-1-primary"
                toggle-color="primary"
                :options="[
                {label: 'Open Jobs', value: false},
                {label: 'Closed Jobs', value: true}
              ]"
              />
            </div>
          </div>
        </template>

        <template v-slot:header="props">
          <template v-if="isEmployer">
            <q-tr :props="props">
              <q-th auto-width>
                Actions
              </q-th>
              <q-th
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                <template v-if="col.name === 'job_title'">
                  <JobTitleHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'job_source'">
                  {{ col.label }}
                  <TableFilter filter-name="Job source"
                               :has-filter="jobsFilter.jobSources && jobsFilter.jobSources.length">
                    <q-select
                      v-model="jobsFilter.jobSources"
                      filled multiple use-chips map-options emit-value autofocus
                      label="Job sources"
                      option-value="val" option-label="label"
                      :options="[
                        { val: 'ats', label: 'Ats' },
                        { val: 'website', label: 'Website' },
                        { val: 'manual', label: 'Manual' },
                      ]"
                    />
                  </TableFilter>
                </template>
                <template v-else-if="col.name === 'job_department'">
                  <JobDepartmentHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'locations'">
                  <LocationsHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'open_date'">
                  <OpenDateHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <span v-else>{{ col.label }}</span>
              </q-th>
            </q-tr>
          </template>
          <template v-else>
            <q-tr :props="props">
              <q-th auto-width class="text-left">
                Share
              </q-th>
              <q-th
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                <template v-if="col.name === 'job_title'">
                  <JobTitleHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'job_department'">
                  <JobDepartmentHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'locations'">
                  <LocationsHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <template v-else-if="col.name === 'open_date'">
                  <OpenDateHeader :col="col" :jobs-filter="jobsFilter"/>
                </template>
                <span v-else>{{ col.label }}</span>
              </q-th>
            </q-tr>
          </template>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <template v-if="isEmployer">
              <q-td auto-width>
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn
                      outline round dense icon="attach_money" color="primary"
                      class="q-mr-xs"
                      @click="openEditJobBonusDialog(props.row)"
                    />
                  </template>
                  Edit referral bonus
                </CustomTooltip>
                <CustomTooltip v-if="props.row.job_source === 'manual'" :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn
                      outline round dense icon="edit" color="primary"
                      @click="openEditJobDialog(props.row)"
                    />
                  </template>
                  Edit job
                </CustomTooltip>
              </q-td>
              <q-td
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                <template v-if="col.name === 'locations'">
                  <LocationsCell :locations="props.row.locations"/>
                </template>
                <template v-else-if="col.name === 'bonus'">
                  <BonusCell :props="props"/>
                </template>
                <template v-else-if="col.name === 'bonus_rule'">
                  <a
                    v-if="!dataUtil.isEmpty(props.row.bonus_rule)"
                    href="#" @click="openShowBonusRuleDialog($event, props.row.bonus_rule.id, props.row.bonus)"
                  >Bonus rule</a>
                  <span v-else-if="props.row.bonus.type === BONUS_TYPES.DEFAULT">Default</span>
                  <span v-else-if="props.row.bonus.type === BONUS_TYPES.DIRECT">Custom</span>
                  <span v-else>None</span>
                </template>
                <span v-else>{{ col.value }}</span>
              </q-td>
            </template>
            <template v-else>
              <q-td auto-width>
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn
                      class="q-mr-xs" color="primary"
                      outline round dense icon="email"
                      @click="openShareJobDialog(props.row, jobsUtil.shareTypes.EMAIL)"/>
                  </template>
                  Send email
                </CustomTooltip>
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn class="q-mr-xs" color="primary" outline round dense
                           @click="openShareJobDialog(props.row, jobsUtil.shareTypes.SMS)" icon="textsms"/>
                  </template>
                  Send text message
                </CustomTooltip>
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn class="q-mr-xs" color="primary" outline round dense
                           @click="openShareJobDialog(props.row, jobsUtil.shareTypes.QR)" icon="qr_code_2"/>
                  </template>
                  Open QR code
                </CustomTooltip>
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>
                    <q-btn color="primary" outline round dense
                           @click="openShareJobDialog(props.row, jobsUtil.shareTypes.LINK)" icon="link"/>
                  </template>
                  Get shareable link
                </CustomTooltip>
              </q-td>
              <q-td
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                <template v-if="col.name === 'locations'">
                  <LocationsCell :locations="props.row.locations"/>
                </template>
                <template v-else-if="col.name === 'bonus'">
                  <BonusCell :props="props"/>
                </template>
                <span v-else>{{ col.value }}</span>
              </q-td>
            </template>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJob from 'components/dialogs/DialogJob.vue'
import DialogJobBonus from 'components/dialogs/DialogJobBonus.vue'
import DialogShareJob from 'components/dialogs/DialogShareJob.vue'
import DialogShowBonusRule from 'components/dialogs/DialogShowBonusRule.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import BonusCell from 'pages/employer/jobs-page/jobs-table/BonusCell.vue'
import JobDepartmentHeader from 'pages/employer/jobs-page/jobs-table/JobDepartmentHeader.vue'
import JobTitleHeader from 'pages/employer/jobs-page/jobs-table/JobTitleHeader.vue'
import LocationsCell from 'pages/employer/jobs-page/jobs-table/LocationsCell.vue'
import LocationsHeader from 'pages/employer/jobs-page/jobs-table/LocationsHeader.vue'
import OpenDateHeader from 'pages/employer/jobs-page/jobs-table/OpenDateHeader.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import { BONUS_TYPES } from 'src/utils/bonus.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import jobsUtil from 'src/utils/jobs.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsSection',
  props: {
    isEmployer: Boolean
  },
  components: {
    BonusCell,
    LocationsCell,
    OpenDateHeader,
    LocationsHeader,
    JobDepartmentHeader,
    CustomTooltip,
    JobTitleHeader,
    TableFilter
  },
  data () {
    return {
      isLoading: false,
      isFetchingJobs: false,
      employer: null,
      employerBonusRules: null,
      dataUtil,
      BONUS_TYPES,
      isClosedJobs: false,
      jobsFilter: {
        jobTitle: null,
        departments: null,
        cities: null,
        states: null,
        countries: null,
        dateRange: null
      },
      jobsUtil
    }
  },
  computed: {
    jobColumns () {
      const columns = [
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
          format: (val) => dateTimeUtil.getShortDate(val)
        },
        {
          name: 'bonus',
          field: row => row.bonus.amount,
          align: 'center',
          label: 'Referral bonus',
          sortable: true,
          sort: (a, b) => parseInt(a) - parseInt(b)
        }
      ]
      if (this.isEmployer) {
        columns.splice(1, 0, {
          name: 'job_source',
          field: 'job_source',
          align: 'left',
          label: 'Source',
          format: dataUtil.capitalize,
          sortable: true
        })
        columns.push({ name: 'bonus_rule', field: 'bonus_rule', align: 'left', label: 'Bonus rule' })
      }
      return columns
    },
    employerJobs () {
      return this.employerStore.getEmployerJobs(this.user.employer_id, { isOnlyClosed: this.isClosedJobs })
    }
  },
  methods: {
    async updateEmployerJobs (isForceRefresh = true) {
      this.isLoading = true
      await Promise.all([
        this.employerStore.setEmployerJobs(this.user.employer_id, { isForceRefresh }),
        this.employerStore.setEmployerJobs(this.user.employer_id, { isForceRefresh, isOnlyClosed: true })
      ])
      this.isLoading = false
    },
    openEditJobDialog (job) {
      if (!this.isEmployer) {
        return
      }
      return this.q.dialog({
        component: DialogJob,
        componentProps: { employerId: this.employer.id, job }
      }).onOk(async () => {
        await this.updateEmployerJobs()
      })
    },
    openEditJobBonusDialog (job) {
      if (!this.isEmployer) {
        return
      }
      return this.q.dialog({
        component: DialogJobBonus,
        componentProps: { jobs: [job] }
      }).onOk(async () => {
        await this.updateEmployerJobs()
      })
    },
    openShowBonusRuleDialog (e, bonusRuleId, bonus) {
      e.preventDefault()
      if (!this.isEmployer) {
        return
      }
      bonusRuleId = parseInt(bonusRuleId)
      const bonusRule = this.employerBonusRules.find((rule) => rule.id === bonusRuleId)
      return this.q.dialog({
        component: DialogShowBonusRule,
        componentProps: { bonusRule, bonus }
      })
    },
    openShareJobDialog (job, shareType) {
      return this.q.dialog({
        component: DialogShareJob,
        componentProps: { job, shareType }
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
      const ruleId = (this.isEmployer) ? parseInt(this.$route.query.ruleId) : null
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
        if (this.jobsFilter.jobSources?.length && !this.jobsFilter.jobSources.includes(job.job_source)) {
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
        if (fromDate && dateTimeUtil.isBefore(job.open_date, fromDate, { isIncludeTime: false })) {
          return false
        }
        if (toDate && dateTimeUtil.isAfter(job.open_date, toDate, { isIncludeTime: false })) {
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
    },
    async updateAtsJobs () {
      this.isFetchingJobs = true
      await this.$api.put('ats/jobs/', getAjaxFormData({ employer_id: this.user.employer_id }))
      await this.updateEmployerJobs()
      this.isFetchingJobs = false
    }
  },
  async mounted () {
    this.isLoading = true
    await Promise.all([
      this.employerStore.setEmployer(this.user.employer_id),
      this.employerStore.setEmployerBonusRules(this.user.employer_id),
      this.updateEmployerJobs(false)
    ])
    this.isLoading = false
    this.employer = this.employerStore.getEmployer(this.user.employer_id)
    this.employerBonusRules = this.employerStore.getEmployerBonusRules(this.user.employer_id)
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
