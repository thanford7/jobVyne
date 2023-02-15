<template>
  <DialogBase
    base-title-text="Send referral request"
    primary-button-text="Send"
    :is-full-screen="true"
    :is-valid-form-fn="isValidForm"
    @ok="sendRequest"
  >
    <q-form ref="form">
      <div class="row q-mt-md">
        <div class="col-md-8 col-12 q-pr-md-sm">
          <q-input
            v-model="emailSubject"
            filled label="Email subject"
            :rules="[
              val => val && val.length > 0 || 'Email subject is required'
            ]"
          />
          <WysiwygEditor2 v-model="emailBody"/>
        </div>
        <div class="col-md-4 col-12 q-pl-md-sm q-gutter-y-md q-mt-md q-mt-md-none">
          <div class="text-bold">
            Email filters
            <CustomTooltip>
              Select the employees you want to send the referral request to.
              If you want to send to all employees, leave the filter empty.
            </CustomTooltip>
          </div>
          <SelectEmployee v-model="userFilters.userIds" :employer-id="employerId" :is-multi="true"/>

          <div>
            <span class="text-bold">Job filters </span>
            <CustomTooltip>
              The unique link shared with each employee will include all jobs matching these filters.
              If you wish to include all jobs, leave the filters blank.
            </CustomTooltip>
            <div>
              <a :href="jobsExampleUrl" target="_blank" class="no-decoration">
                <span class="text-gray-3">
                  <q-icon name="launch"/>&nbsp;
                </span>
                  View {{ dataUtil.pluralize('job', filteredJobs.length) }}
              </a>
            </div>
          </div>
          <SelectJobDepartment v-model="jobFilters.department_ids" :is-emit-id="true"/>
          <SelectJobCity v-model="jobFilters.city_ids" :is-emit-id="true"/>
          <SelectJobState v-model="jobFilters.state_ids" :is-emit-id="true"/>
          <SelectJobCountry v-model="jobFilters.country_ids" :is-emit-id="true"/>
          <SelectJob v-model="jobFilters.job_ids" :employer-id="employerId"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectEmployee from 'components/inputs/SelectEmployee.vue'
import SelectJob from 'components/inputs/SelectJob.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'

export default {
  name: 'DialogShareJobLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    SelectJob,
    SelectJobCountry,
    SelectJobState,
    SelectJobCity,
    SelectJobDepartment,
    DialogBase,
    WysiwygEditor2,
    CustomTooltip,
    SelectEmployee
  },
  props: {
    employerId: [Number, String]
  },
  data () {
    return {
      emailSubject: '',
      emailBody: '',
      filteredJobs: [],
      filteredJobsCache: {},
      userFilters: {
        userIds: null
      },
      jobFilters: {
        department_ids: [],
        city_ids: [],
        state_ids: [],
        country_ids: [],
        job_ids: []
      },
      dataUtil
    }
  },
  computed: {
    jobsExampleUrl () {
      return dataUtil.getUrlWithParams({
        path: `/jobs-link/example/${this.employerId}`,
        isExcludeExistingParams: true,
        addParams: Object.entries(this.jobFilters).reduce((addParams, [filterKey, filterVal]) => {
          if (!filterVal || !filterVal.length) {
            return addParams
          }
          addParams.push({ key: filterKey, val: filterVal })
          return addParams
        }, [])
      })
    }
  },
  watch: {
    jobFilters: {
      async handler () {
        await this.getFilteredJobs()
      },
      deep: true
    }
  },
  methods: {
    async getFilteredJobs () {
      const params = { employer_id: this.employerId, ...this.jobFilters }
      const cacheKey = JSON.stringify(params)
      const cachedFilteredJobs = this.filteredJobsCache[cacheKey]
      if (cachedFilteredJobs) {
        this.filteredJobs = cachedFilteredJobs
      } else {
        const jobResp = await this.$api.get('employer/job/', { params })
        this.filteredJobs = jobResp.data
        this.filteredJobsCache[cacheKey] = jobResp.data
      }
    },
    async isValidForm () {
      return await this.$refs.form.validate()
    },
    async sendRequest () {
      //
    }
  },
  async mounted () {
    await this.getFilteredJobs()
  }
}
</script>
