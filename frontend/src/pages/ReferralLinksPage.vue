<template>
  <q-page padding>
    <div class="q-ml-sm">
      <div class="row q-pb-sm border-bottom-2-gray-300">
        <h5 class="text-gray-900">Referral links</h5>
        <p class="text-gray-500 q-mt-none">
          Add one or more referral links to your social media accounts. Anyone that visits your page can click on the
          link
          and will be directed to a webpage with all open jobs at your company. If they apply and work at your company,
          you can collect a referral bonus!
        </p>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            1
          </div>
          <h6 style="display: inline-block;">Select the platform where you will display the link</h6>
        </div>
        <div class="col-12">
          <q-select
            outlined
            v-model="formData.platform"
            :emit-value="true"
            :options="socialStore.platforms"
            option-value="name"
            option-label="name"
            label="Platform"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            2
          </div>
          <h6 style="display: inline-block;">Add filters for the jobs to display when the link is clicked</h6>
        </div>
        <div class="col-12">
          <div class="row">
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-select
                outlined multiple clearable use-chips
                v-model="formData.departments"
                :emit-value="true"
                :options="employerStore.getJobDepartments"
                option-value="department"
                option-label="department"
                label="Department"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-select
                outlined multiple clearable use-chips
                v-model="formData.cities"
                :emit-value="true"
                :options="employerStore.getJobCities"
                option-value="city"
                option-label="city"
                label="City"
              />
            </div>
            <div class="col-12 col-md-6 q-pr-md-sm">
              <q-select
                outlined multiple clearable use-chips
                v-model="formData.states"
                :emit-value="true"
                :options="employerStore.getJobStates"
                option-value="state"
                option-label="state"
                label="State"
              />
            </div>
            <div class="col-12 col-md-6">
              <q-select
                outlined multiple clearable use-chips
                v-model="formData.countries"
                :emit-value="true"
                :options="employerStore.getJobCountries"
                option-value="country"
                option-label="country"
                label="Country"
              />
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
            :rows="employerStore.getEmployerJobs"
            row-key="id"
            :columns="jobColumns"
            :filter-method="jobDataFilter"
            filter="formData"
            no-data-label="No jobs match the filter"
            :rows-per-page-options="[5, 10, 15]"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="circle bg-gray-300 q-mr-sm" style="display: inline-block;">
            4
          </div>
          <h6 style="display: inline-block;">Posting instructions</h6>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { useEmployerStore } from 'stores/employer-store'
import { useSocialStore } from 'stores/social-store'
import dataUtil from 'src/utils/data'
import dateTimeUtil from 'src/utils/datetime'

const jobColumns = [
  { name: 'job_title', field: 'job_title', required: true, align: 'left', label: 'Title', sortable: true },
  { name: 'job_department', field: 'job_department', align: 'left', label: 'Department', sortable: true },
  { name: 'location', field: 'location', align: 'left', label: 'Location', sortable: true },
  {
    name: 'open_date',
    field: 'open_date',
    align: 'left',
    label: 'Posted Date',
    sortable: true,
    format: dateTimeUtil.getShortDate
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

export default {
  data () {
    return {
      formData: {
        platform: null,
        departments: null,
        cities: null,
        states: null,
        countries: null
      },
      jobColumns
    }
  },
  methods: {
    jobDataFilter (rows) {
      return rows.filter((job) => {
        if (this.formData.departments?.length && !this.formData.departments.includes(job.job_department)) {
          return false
        }
        if (this.formData.cities?.length && !this.formData.cities.includes(job.city)) {
          return false
        }
        if (this.formData.states?.length && !this.formData.states.includes(job.state)) {
          return false
        }
        if (this.formData.countries?.length && !this.formData.countries.includes(job.country)) {
          return false
        }
        return true
      })
    }
  },
  setup () {
    const socialStore = useSocialStore()
    const employerStore = useEmployerStore()
    socialStore.setPlatforms()
    employerStore.setEmployer()
    employerStore.setEmployerJobs()
    return { socialStore, employerStore }
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
