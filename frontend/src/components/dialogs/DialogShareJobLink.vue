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
          <BaseExpansionItem
            title="Placeholder content" class="content-expansion q-mt-md"
            :is-include-separator="false"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                This content will be filled in dynamically based on the employee's unique
                link and the job filters.
              </CustomTooltip>
            </template>
            <q-table
              dense flat
              :hide-bottom="true"
              :columns="placeholderTableColumns"
              :rows="placeholderTableRows"
            >
              <template v-slot:body-cell-action="props">
                <q-td>
                  <q-btn
                    unelevated dense label="Add" color="grey-6"
                    @click="addContent(props.row.placeholder)"
                  />
                </q-td>
              </template>
            </q-table>
          </BaseExpansionItem>
        </div>
        <div class="col-md-4 col-12 q-pl-md-sm q-mt-md q-mt-md-none">
          <BaseExpansionItem
            :is-include-separator="false"
            title="Email filters" class="content-expansion"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                Select the employees you want to send the referral request to.
                If you want to send to all employees, leave the filter empty.
              </CustomTooltip>
            </template>
            <SelectEmployee
              v-model="userFilters.user_ids"
              class="q-mb-md"
              :employer-id="employerId" :is-multi="true"
            />
          </BaseExpansionItem>
          <BaseExpansionItem
            :is-include-separator="false"
            title="Job filters" class="content-expansion"
          >
            <template v-slot:header>
              <CustomTooltip :is_include_space="true">
                The unique link shared with each employee will include all jobs matching these filters.
                If you wish to include all jobs, leave the filters blank.
              </CustomTooltip>
            </template>
            <div>
              <a :href="jobsExampleUrl" target="_blank" class="no-decoration">
                <span class="text-gray-3">
                  <q-icon name="launch"/>&nbsp;
                </span>
                View {{ dataUtil.pluralize('job', filteredJobs.length) }}
              </a>
            </div>
            <div class="q-gutter-y-sm q-mt-md">
              <SelectJobDepartment v-model="jobFilters.department_ids" :is-emit-id="true"/>
              <SelectJobCity v-model="jobFilters.city_ids" :is-emit-id="true"/>
              <SelectJobState v-model="jobFilters.state_ids" :is-emit-id="true"/>
              <SelectJobCountry v-model="jobFilters.country_ids" :is-emit-id="true"/>
              <SelectJob v-model="jobFilters.job_ids" :employer-id="employerId"/>
            </div>
          </BaseExpansionItem>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import BaseExpansionItem from 'components/BaseExpansionItem.vue'
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
import { getAjaxFormData } from 'src/utils/requests.js'
import { useEmployerStore } from 'stores/employer-store.js'

// Keep in sync with ContentPlaceholders on SocialPost backend
const REFERRAL_CONTENT_PLACEHOLDERS = {
  JOB_LINK: '{{link}}',
  JOBS_LIST: '{{jobs-list}}',
  EMPLOYEE_FIRST_NAME: '{{first-name}}',
  EMPLOYEE_LAST_NAME: '{{last-name}}'
}

const placeholderTableColumns = [
  { name: 'action', field: 'action', align: 'center' },
  { name: 'name', field: 'name', align: 'left', label: 'Name' },
  { name: 'placeholder', field: 'placeholder', align: 'left', label: 'Placeholder' },
  { name: 'example', field: 'example', align: 'left', label: 'Example', style: 'white-space: pre-line;' }
]
const placeholderTableRows = [
  { name: 'Employee first name', placeholder: REFERRAL_CONTENT_PLACEHOLDERS.EMPLOYEE_FIRST_NAME, example: 'Jake' },
  { name: 'Employee last name', placeholder: REFERRAL_CONTENT_PLACEHOLDERS.EMPLOYEE_LAST_NAME, example: 'Smith' },
  {
    name: 'Jobs page link',
    placeholder: REFERRAL_CONTENT_PLACEHOLDERS.JOB_LINK,
    example: 'www.jobvyne.com/jobs-link/ad8audafdi'
  },
  {
    name: 'Open jobs list',
    placeholder: REFERRAL_CONTENT_PLACEHOLDERS.JOBS_LIST,
    example: '- Software engineer\n- Product manager\n- Market analyst'
  }
]

export default {
  name: 'DialogShareJobLink',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    BaseExpansionItem,
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
      employer: null,
      emailSubject: '',
      emailBody: '',
      filteredJobs: [],
      filteredJobsCache: {},
      userFilters: {
        user_ids: null
      },
      jobFilters: {
        department_ids: [],
        city_ids: [],
        state_ids: [],
        country_ids: [],
        job_ids: []
      },
      placeholderTableRows,
      placeholderTableColumns,
      employerStore: null,
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
    addContent (content) {
      if (!this.emailBody) {
        this.emailBody = ''
      }
      this.emailBody += content
    },
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
      const formData = {
        employer_id: this.employerId,
        email_subject: this.emailSubject,
        email_body: this.emailBody,
        ...this.jobFilters,
        ...this.userFilters
      }
      await this.$api.post('employer/referral/request/', getAjaxFormData(formData))
      await this.employerStore.setEmployerReferralRequests(this.employerId, true)
      this.$emit('ok')
    }
  },
  async mounted () {
    this.employerStore = useEmployerStore()
    await Promise.all([
      this.getFilteredJobs(),
      this.employerStore.setEmployer(this.employerId)
    ])
    this.employer = this.employerStore.getEmployer(this.employerId)
    this.emailSubject = `Help us hire at ${this.employer.name}! Share your personal referral link`
    this.emailBody = `
      <p>Hi {{first-name}},</p>
      <p>
        We are using JobVyne to help hire for ${this.employer.name}. The link below is personalized
        specifically for you and allows anyone to click the link to view and apply for open jobs at
        our company including:
      </p>
      <p>${REFERRAL_CONTENT_PLACEHOLDERS.JOBS_LIST}</p>
      <p>
        Please help us hire by sharing your personal referral link directly with your professional network
        and also across professional social media sites like LinkedIn.
      </p>
      <p>
        Your referral link: ${REFERRAL_CONTENT_PLACEHOLDERS.JOB_LINK}
      </p>
      <p>
        Thanks for helping us grow!
      </p>
    `
  }
}
</script>
