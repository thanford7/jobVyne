<template>
  <div class="row q-gutter-y-md" style="min-width: 500px;">
    <div class="col-12">
      <q-table
        :loading="isLoading"
        :rows="jobs"
        :columns="jobColumns"
        row-key="id"
        :rows-per-page-options="[25, 50]"
        v-model:pagination="pagination"
        :filter="jobsFilter"
        @request="fetchJobs"
      >
        <template v-slot:top>
          <a v-if="hasFilter" href="#" @click.prevent="clearJobsFilter()">Reset filters</a>
        </template>
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
            >
              <template v-if="col.name === 'employer_name'">
                {{ col.label }}
                <TableFilter
                  filter-name="Employer"
                  :has-filter="dataUtil.getBoolean(jobsFilter.employers && jobsFilter.employers.length)"
                >
                  <SelectEmployer v-model="jobsFilter.employers" :employers="employers" :is-multi="true"/>
                </TableFilter>
              </template>
              <template v-if="col.name === 'job_department'">
                {{ col.label }}
                <TableFilter
                  filter-name="Job department"
                  :has-filter="dataUtil.getBoolean(jobsFilter.job_departments && jobsFilter.job_departments.length)"
                >
                  <SelectJobDepartment v-model="jobsFilter.job_departments" :is-multi="true" :is-all="true" :is-emit-id="true"/>
                </TableFilter>
              </template>
              <template v-if="col.name === 'job_title'">
                {{ col.label }}
                <TableFilter
                  filter-name="Job title"
                  :has-filter="dataUtil.getBoolean(jobsFilter.job_title)"
                >
                  <q-input v-model="jobsFilter.job_title" filled label="Job title"/>
                </TableFilter>
              </template>
              <template v-if="col.name === 'locations'">
                {{ col.label }}
                <TableFilter
                  filter-name="Location"
                  :has-filter="dataUtil.getBoolean(jobsFilter.locations && jobsFilter.locations.length)"
                >
                  <SelectLocation v-model="jobsFilter.locations" :is-multi="true" :locations="locations"/>
                </TableFilter>
              </template>
              <template v-if="col.name === 'employment_type'">
                {{ col.label }}
                <TableFilter
                  filter-name="Employment type"
                  :has-filter="dataUtil.getBoolean(jobsFilter.employment_types && jobsFilter.employment_types.length)"
                >
                  <q-select
                    v-model="jobsFilter.employment_types"
                    filled label="Employment type"
                    :options="employmentTypes.map((et) => ({ val: et }))"
                    option-value="val"
                    option-label="val"
                    multiple map-options emit-value use-chips
                  />
                </TableFilter>
              </template>
            </q-th>
          </q-tr>
        </template>
        <template v-slot:body-cell-job_title="props">
          <q-td
            key="job_title"
            :props="props"
            :title="props.row.job_title"
          >
            {{ dataUtil.truncateText(props.row.job_title, 30) }}
          </q-td>
        </template>
        <template v-slot:body-cell-locations="props">
          <q-td
            key="locations"
            :props="props"
          >
            <LocationsCell :locations="props.row.locations"/>
          </q-td>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectLocation from 'components/inputs/SelectLocation.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import dataUtil from 'src/utils/data.js'
import LocationsCell from 'pages/employer/jobs-page/jobs-table/LocationsCell.vue'
import { useJobsStore } from 'stores/jobs-store.js'

const jobColumns = [
  { name: 'employer_name', field: 'employer_name', align: 'left', label: 'Employer', sortable: true },
  { name: 'job_department', field: 'job_department', align: 'left', label: 'Department', sortable: true },
  { name: 'job_title', field: 'job_title', align: 'left', label: 'Job title', sortable: true },
  { name: 'locations', field: 'locations', align: 'left', label: 'Location', sortable: true },
  { name: 'employment_type', field: 'employment_type', align: 'left', label: 'Employment type', sortable: true }
]

const jobsFilterTemplate = {
  employers: null,
  job_departments: null,
  job_title: null,
  locations: null,
  employment_types: null
}

const pagination = {
  sortBy: null,
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: null
}

export default {
  name: 'EmployerSection',
  components: { SelectLocation, SelectJobDepartment, SelectEmployer, LocationsCell, TableFilter },
  data () {
    return {
      isLoading: false,
      jobColumns,
      jobs: [],
      employers: null,
      locations: null,
      employmentTypes: null,
      pagination,
      jobsFilter: { ...jobsFilterTemplate },
      jobsStore: useJobsStore(),
      dataUtil
    }
  },
  computed: {
    hasFilter () {
      return !dataUtil.isDeepEqual(jobsFilterTemplate, this.jobsFilter)
    }
  },
  methods: {
    clearJobsFilter () {
      this.jobsFilter = { ...jobsFilterTemplate }
    },
    async fetchJobs ({ pagination = this.pagination, filter = this.jobsFilter } = {}) {
      this.isLoading = true
      await this.jobsStore.setJobs(pagination, { filterParams: filter })
      const data = this.jobsStore.getJobs(pagination, filter)
      const { jobs, employers, locations, employment_types: employmentTypes, total_job_count: totalJobCount } = data
      this.jobs = jobs
      this.employers = employers
      this.locations = locations
      this.employmentTypes = employmentTypes
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = totalJobCount
      this.isLoading = false
    }
  },
  async mounted () {
    await this.fetchJobs()
  }
}
</script>
