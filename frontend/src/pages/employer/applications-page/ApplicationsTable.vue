<template>
  <q-table
    :loading="isLoading"
    :rows="applications"
    :columns="applicationColumns"
    row-key="id"
    :rows-per-page-options="[25]"
    v-model:pagination="pagination"
    :filter="applicationFilter"
    @request="fetchApplications"
  >
    <template v-slot:top>
      <div class="row w-100 items-center">
        <div class="q-ml-md" style="display: inline-block">
          <a href="#" @click="clearApplicationFilter">Clear all filters</a>
        </div>
        <q-space/>
        <DateRangeSelector v-model="dateRange" :is-clearable="false" placeholder="Submission date"/>
      </div>
    </template>
    <template v-slot:header-cell-applicant="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Applicant"
                     :has-filter="dataUtil.getBoolean(applicationFilter.applicantName && applicationFilter.applicantName.length)">
          <q-input filled borderless debounce="300" v-model="applicationFilter.applicantName" placeholder="Applicant name">
            <template v-slot:append>
              <q-icon name="search"/>
            </template>
          </q-input>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-email="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Email"
                     :has-filter="dataUtil.getBoolean(applicationFilter.applicantEmail && applicationFilter.applicantEmail.length)">
          <q-input filled borderless debounce="300" v-model="applicationFilter.applicantEmail" placeholder="Applicant email">
            <template v-slot:append>
              <q-icon name="search"/>
            </template>
          </q-input>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-job_title="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Job title"
                     :has-filter="dataUtil.getBoolean(applicationFilter.jobTitle && applicationFilter.jobTitle.length)">
          <q-input filled borderless debounce="300" v-model="applicationFilter.jobTitle" placeholder="Job title">
            <template v-slot:append>
              <q-icon name="search"/>
            </template>
          </q-input>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-locations="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Location"
                     :has-filter="dataUtil.getBoolean(applicationFilter.locations && applicationFilter.locations.length)">
          <SelectLocation v-model="applicationFilter.locations" :is-multi="true" :locations="locations"/>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:header-cell-referrer="props">
      <q-th :props="props">
        {{ props.col.label }}
        <TableFilter filter-name="Referrer"
                     :has-filter="dataUtil.getBoolean(applicationFilter.referrerName && applicationFilter.referrerName.length)">
          <q-input filled borderless debounce="300" v-model="applicationFilter.referrerName" placeholder="Referrer name">
            <template v-slot:append>
              <q-icon name="search"/>
            </template>
          </q-input>
        </TableFilter>
      </q-th>
    </template>
    <template v-slot:body-cell-applicant="props">
      <q-td class="text-center" :props="props">
        {{ props.row.first_name }} {{ props.row.last_name }}
      </q-td>
    </template>
    <template v-slot:body-cell-referrer="props">
      <q-td class="text-center" :props="props">
        {{ props.row.owner_first_name }} {{ props.row.owner_last_name }}
      </q-td>
    </template>
    <template v-slot:body-cell-locations="props">
      <q-td :props="props">
        <template v-if="props.row.locations.length > 1">
          <CustomTooltip>
            <template v-slot:icon>
              <q-chip
                color="grey-7" text-color="white" size="md" icon="place"
              >
                Multiple locations
              </q-chip>
            </template>
            <ul>
              <li v-for="location in props.row.locations">
                {{ locationUtil.getFullLocation(location) }}
              </li>
            </ul>
          </CustomTooltip>
        </template>
        <q-chip
          v-else-if="props.row.locations.length"
          color="grey-7" text-color="white" size="md" icon="place"
        >
          {{ locationUtil.getFullLocation(props.row.locations[0]) }}
        </q-chip>
        <div v-else>None</div>
      </q-td>
    </template>
    <template v-slot:body-cell-linkedin_url="props">
      <q-td :props="props">
        <a v-if="props.value" :href="props.value" target="_blank" class="no-decoration">
          <span class="text-gray-3">
            <q-icon name="launch"/>&nbsp;
          </span>
          LinkedIn Profile
        </a>
        <div v-else>None</div>
      </q-td>
    </template>
    <template v-slot:body-cell-resume_url="props">
      <q-td :props="props">
        <a v-if="props.value" :href="props.value" target="_blank" class="no-decoration">
          <span class="text-gray-3 no-decoration">
            <q-icon name="launch"/>&nbsp;
          </span>
          Resume
        </a>
        <div v-else>None</div>
      </q-td>
    </template>
  </q-table>
</template>

<script>

import CustomTooltip from 'components/CustomTooltip.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import SelectLocation from 'components/inputs/SelectLocation.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

const applicationFilterTemplate = {
  applicantName: null,
  applicantEmail: null,
  referrerName: null,
  locations: null,
  jobTitle: null
}

const pagination = {
  sortBy: 'created_dt',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: null
}

const defaultDateRange = {
  from: dateTimeUtil.addDays(new Date(), -6, true),
  to: new Date()
}

export default {
  name: 'ApplicationsTable',
  components: { TableFilter, SelectLocation, CustomTooltip, DateRangeSelector },
  data () {
    return {
      isLoading: true,
      applications: [],
      locations: [],
      applicationFilter: { ...applicationFilterTemplate },
      pagination,
      dateRange: { ...defaultDateRange },
      dataUtil,
      locationUtil
    }
  },
  watch: {
    dateRange: {
      async handler () {
        if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
          this.dateRange = { ...defaultDateRange }
        }
        await this.fetchApplications()
      }
    }
  },
  computed: {
    applicationColumns () {
      return [
        { name: 'applicant', field: 'first_name', align: 'left', label: 'Applicant', sortable: true },
        { name: 'job_title', field: 'job_title', align: 'left', label: 'Job', sortable: true },
        { name: 'locations', field: 'locations', align: 'left', label: 'Job Locations' },
        { name: 'email', field: 'email', align: 'left', label: 'Email', sortable: true },
        {
          name: 'phone_number',
          field: 'phone_number',
          align: 'left',
          label: 'Phone Number',
          format: (val) => val || 'None'
        },
        { name: 'linkedin_url', field: 'linkedin_url', align: 'left', label: 'LinkedIn' },
        { name: 'resume_url', field: 'resume_url', align: 'left', label: 'Resume' },
        {
          name: 'created_dt',
          field: 'created_dt',
          align: 'left',
          label: 'Submission Date',
          format: dateTimeUtil.getShortDate.bind(dateTimeUtil),
          sortable: true
        },
        { name: 'referrer', field: 'owner_first_name', align: 'left', label: 'Referrer', sortable: true }
      ]
    }
  },
  methods: {
    clearApplicationFilter () {
      this.applicationFilter = { ...applicationFilterTemplate }
    },
    async fetchApplications ({ pagination = this.pagination, filter = this.applicationFilter } = {}) {
      if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
        return {}
      }
      this.isLoading = true
      const paginatedApplications = await this.dataStore.getApplications(
        this.dateRange.from,
        this.dateRange.to,
        {
          employer_id: this.authStore.propUser.employer_id,
          is_raw_data: true,
          filter_by: JSON.stringify(filter),
          page_count: pagination.page,
          sort_order: pagination.sortBy,
          is_descending: pagination.descending
        }
      )
      this.applications = paginatedApplications.applications || []
      this.locations = paginatedApplications.locations || []
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = paginatedApplications.total_application_count
      this.isLoading = false
    }
  },
  async mounted () {
    await this.fetchApplications()
  },
  setup () {
    return {
      authStore: useAuthStore(),
      dataStore: useDataStore()
    }
  }
}
</script>
