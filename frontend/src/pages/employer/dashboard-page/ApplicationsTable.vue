<template>
  <div v-if="isInitLoaded">
    <div class="text-bold q-pb-sm border-bottom-1-gray-300">
      Applications
    </div>
    <div class="row q-my-sm items-end q-gutter-y-md">
      <div class="col-12 col-md-6">
        <div class="row">
          <div class="col-12 text-small q-mb-xs">
            Group by:
          </div>
          <div class="col-12">
            <q-btn-group rounded unelevated>
              <q-btn
                v-for="option in GROUP_OPTIONS"
                :color="(chartGroups.includes(option.key)) ? 'grey-8' : 'grey-6'"
                rounded :label="option.label"
                @click="toggleGroup(option.key)"
              />
            </q-btn-group>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-6">
        <DateRangeSelector
          dense
          v-model="dateRange"
          placeholder="Date range"
          :is-clearable="false"
          class="q-ml-md"
          style="min-width: 250px;"
        />
      </div>
    </div>
    <q-table
      ref="table"
      @mounted="$refs.table.sort('applicationDT')"
      flat
      :rows="applications"
      :columns="columns"
      :rows-per-page-options="[25, 50, 100]"
    >
      <template v-slot:header-cell-ownerName="props">
        <q-th :props="props">
          {{ props.col.label }}
          <TableFilter filter-name="Employee" :has-filter="boolean(chartFilters.employees && chartFilters.employees.length)">
            <q-select
              filled use-input use-chips multiple emit-value map-options
              label="Employee"
              v-model="chartFilters.employees"
              @filter="employeeOptionsFilter"
              :options="employees"
              option-value="id"
              option-label="name"
            />
          </TableFilter>
        </q-th>
      </template>
      <template v-slot:header-cell-platformName="props">
        <q-th :props="props">
          {{ props.col.label }}
          <TableFilter filter-name="Platform" :has-filter="boolean(chartFilters.platforms && chartFilters.platforms.length)">
            <q-select
              filled use-input use-chips multiple emit-value map-options
              label="Platform"
              v-model="chartFilters.platforms"
              :options="platforms"
              option-value="name"
              option-label="name"
            />
          </TableFilter>
        </q-th>
      </template>
      <template v-slot:header-cell-jobTitle="props">
        <q-th :props="props">
          {{ props.col.label }}
          <TableFilter filter-name="Job title" :has-filter="boolean(chartFilters.jobTitle && chartFilters.jobTitle.length)">
            <q-input filled borderless debounce="300" v-model="chartFilters.jobTitle" placeholder="Job title">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>
          </TableFilter>
        </q-th>
      </template>
    </q-table>
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

const GROUP_OPTIONS = [
  { key: 'EMPLOYEE', label: 'Employee', field: 'owner_full_name' },
  { key: 'PLATFORM', label: 'Platform', field: 'platform_name' },
  { key: 'JOB_TITLE', label: 'Job Title', field: 'job_title' },
  { key: 'DATE', label: 'Date', field: 'date' }
]

export default {
  name: 'ApplicationsTable',
  components: { ChartSkeleton, DateRangeSelector, TableFilter },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      chartRawData: null,
      GROUP_OPTIONS,
      GROUP_KEY_EMPLOYEE: 'EMPLOYEE',
      GROUP_KEY_PLATFORM: 'PLATFORM',
      GROUP_KEY_JOB_TITLE: 'JOB_TITLE',
      GROUP_KEY_DATE: 'DATE',
      chartGroups: [],
      chartFilters: {
        employees: [],
        platforms: [],
        jobTitle: null
      },
      employeeFilterText: null,
      dateRange: {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      }
    }
  },
  computed: {
    applications () {
      if (!this.chartRawData) {
        return []
      }
      let chartData = this.filterApplications(this.chartRawData)
      if (this.chartGroups.length) {
        chartData = dataUtil.groupBy(chartData, this.makeApplicationKey)
        chartData = Object.entries(chartData).reduce((chartData, [applicationKey, groupedApps]) => {
          chartData.push({
            ...this.hydrateApplicationKey(applicationKey),
            applicationCount: groupedApps.length
          })
          return chartData
        }, [])
      }
      return chartData
    },
    columns () {
      let columns = [
        { name: 'ownerName', field: 'owner_full_name', label: 'Employee', align: 'left', sortable: true },
        { name: 'platformName', field: 'platform_name', label: 'Platform', align: 'left', sortable: true },
        { name: 'jobTitle', field: 'job_title', label: 'Job Title', align: 'left', sortable: true },
        { name: 'applicantName', field: 'applicant_full_name', label: 'Applicant', align: 'left', sortable: true },
        {
          name: 'applicationDT',
          field: 'date',
          label: 'Application Date',
          align: 'left',
          sortable: true
        }
      ]

      if (!this.chartGroups.length) {
        return columns
      }
      const groupFields = this.chartGroups.map((groupKey) => GROUP_OPTIONS.find((o) => o.key === groupKey).field)
      columns = columns.filter((column) => groupFields.includes(column.field))
      columns.push({
        name: 'applicationCount',
        field: 'applicationCount',
        label: 'Application Count',
        align: 'center',
        sortable: true
      })
      return columns
    },
    employees () {
      let employees = this.chartRawData.map((app) => ({ id: app.owner_id, name: app.owner_full_name }))
      employees = dataUtil.sortBy(dataUtil.uniqBy(employees, 'id'), 'name')
      if (!this.employeeFilterText || this.employeeFilterText === '') {
        return employees
      }
      const filterRegex = new RegExp(`.*?${this.employeeFilterText}.*?`, 'i')
      return employees.filter((e) => e.name.match(filterRegex))
    },
    platforms () {
      const platforms = this.chartRawData.map((app) => ({ name: app.platform_name }))
      return dataUtil.sortBy(dataUtil.uniqBy(platforms, 'name'), 'name')
    }
  },
  watch: {
    dateRange () {
      this.setChartRawData()
    }
  },
  methods: {
    boolean (val) {
      return Boolean(val)
    },
    employeeOptionsFilter (filterTxt, update) {
      update(() => {
        this.employeeFilterText = filterTxt
      })
    },
    filterApplications (applications) {
      return applications.filter((app) => {
        if (
          this.chartFilters.employees &&
          this.chartFilters.employees.length &&
          !this.chartFilters.employees.includes(app.owner_id)
        ) {
          return false
        }
        if (
          this.chartFilters.platforms &&
          this.chartFilters.platforms.length &&
          !this.chartFilters.platforms.includes(app.platform_name)
        ) {
          return false
        }
        if (this.chartFilters.jobTitle && this.chartFilters.jobTitle.length) {
          const jobTitleRegex = new RegExp(`.*?${this.chartFilters.jobTitle}.*?`, 'i')
          if (!app.job_title.match(jobTitleRegex)) {
            return false
          }
        }
        return true
      })
    },
    makeApplicationKey (application) {
      return JSON.stringify(this.chartGroups.reduce((applicationKey, groupKey) => {
        const groupOption = this.GROUP_OPTIONS.find((o) => o.key === groupKey)
        applicationKey.push(application[groupOption.field])
        return applicationKey
      }, []))
    },
    hydrateApplicationKey (applicationKey) {
      const applicationValues = JSON.parse(applicationKey)
      return applicationValues.reduce((applicationData, appValue, idx) => {
        const groupOption = this.GROUP_OPTIONS.find((o) => o.key === this.chartGroups[idx])
        applicationData[groupOption.field] = appValue
        return applicationData
      }, {})
    },
    toggleFilter (filterKey) {
      if (this.chartFilters.includes(filterKey)) {
        dataUtil.removeItemFromList(this.chartFilters, { itemFindFn: (item) => item === filterKey })
      } else {
        this.chartFilters.push(filterKey)
      }
    },
    toggleGroup (groupKey) {
      if (this.chartGroups.includes(groupKey)) {
        dataUtil.removeItemFromList(this.chartGroups, { itemFindFn: (item) => item === groupKey })
      } else {
        this.chartGroups.push(groupKey)
      }
    },
    async setChartRawData () {
      if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
        return {}
      }
      this.isLoading = true
      this.chartRawData = await this.dataStore.getApplications(
        this.dateRange.from,
        this.dateRange.to,
        { employerId: this.authStore.propUser.employer_id }
      )
      this.chartRawData = this.chartRawData || []
      this.isLoading = false
      this.chartRawData.forEach((application) => {
        application.owner_full_name = `${application.owner_first_name} ${application.owner_last_name}`
        application.applicant_full_name = `${application.first_name} ${application.last_name}`
        application.date = dateTimeUtil.getShortDate(application.date)
      })
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.dataStore = useDataStore()
    await this.authStore.setUser()
    await this.setChartRawData()
    this.isInitLoaded = true
  }
}
</script>
