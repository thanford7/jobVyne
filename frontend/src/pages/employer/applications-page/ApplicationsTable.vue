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
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th auto-width/>
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <template v-if="col.name === 'applicant'">
            {{ col.label }}
            <TableFilter filter-name="Applicant"
                         :has-filter="dataUtil.getBoolean(applicationFilter.applicantName && applicationFilter.applicantName.length)">
              <q-input filled borderless debounce="300" v-model="applicationFilter.applicantName"
                       placeholder="Applicant name">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'email'">
            {{ col.label }}
            <TableFilter filter-name="Email"
                         :has-filter="dataUtil.getBoolean(applicationFilter.applicantEmail && applicationFilter.applicantEmail.length)">
              <q-input filled borderless debounce="300" v-model="applicationFilter.applicantEmail"
                       placeholder="Applicant email">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'job_title'">
            {{ col.label }}
            <TableFilter filter-name="Job title"
                         :has-filter="dataUtil.getBoolean(applicationFilter.jobTitle && applicationFilter.jobTitle.length)">
              <q-input filled borderless debounce="300" v-model="applicationFilter.jobTitle" placeholder="Job title">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'locations'">
            {{ col.label }}
            <TableFilter filter-name="Location"
                         :has-filter="dataUtil.getBoolean(applicationFilter.locations && applicationFilter.locations.length)">
              <SelectLocation v-model="applicationFilter.locations" :is-multi="true" :locations="locations"/>
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'recommended'">
            {{ col.label }}
            <TableFilter filter-name="Recommended"
                         :has-filter="dataUtil.getBoolean(applicationFilter.recommended && applicationFilter.recommended.length)">
              <q-select
                v-model="applicationFilter.recommended"
                filled emit-value map-options multiple use-chips
                :options="applicantFeedbackUtil.getRecommendApplicantOpts()"
                option-value="val"
                option-label="label"
                label="Would you recommend?"
              />
            </TableFilter>
          </template>
          <template v-else-if="col.name === 'referrer'">
            {{ col.label }}
            <TableFilter filter-name="Referrer"
                         :has-filter="dataUtil.getBoolean(applicationFilter.referrerName && applicationFilter.referrerName.length)">
              <q-input filled borderless debounce="300" v-model="applicationFilter.referrerName"
                       placeholder="Referrer name">
                <template v-slot:append>
                  <q-icon name="search"/>
                </template>
              </q-input>
            </TableFilter>
          </template>
          <span v-else>{{ col.label }}</span>
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <q-btn
            size="sm" color="gray-500" class="q-mr-sm" round dense
            @click="props.expand = !props.expand"
            :icon="props.expand ? 'expand_less' : 'expand_more'" title="Expand details"
          />
          <q-btn
            size="sm" color="primary" dense
            :icon="(hasApplicationFeedback(props.row)) ? 'edit' : 'add'"
            :label="`${(hasApplicationFeedback(props.row)) ? 'Edit' : 'Add'} review `"
            @click="openReviewDialog(props.row)"
          />
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <template v-if="col.name === 'applicant'">
            <q-icon
              v-if="getIsNotificationFailure(props.row)"
              name="error" color="negative" size="24px"
              title="Notification failure"
            />
            {{ props.row.first_name }} {{ props.row.last_name }}
          </template>
          <template v-else-if="col.name === 'referrer'">
            {{ props.row.owner_first_name }} {{ props.row.owner_last_name }}
          </template>
          <template v-else-if="col.name === 'locations'">
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
          </template>
          <template v-else-if="col.name === 'linkedin_url'">
            <a v-if="col.value" :href="col.value" target="_blank" class="no-decoration">
            <span class="text-gray-3">
              <q-icon name="launch"/>&nbsp;
            </span>
              LinkedIn Profile
            </a>
            <div v-else>None</div>
          </template>
          <template v-else-if="col.name === 'resume_url'">
            <a v-if="col.value" :href="col.value" target="_blank" class="no-decoration">
            <span class="text-gray-3 no-decoration">
              <q-icon name="launch"/>&nbsp;
            </span>
              Resume
            </a>
            <div v-else>None</div>
          </template>
          <span v-else>{{ col.value }}</span>
        </q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
          <div class="text-bold q-mb-sm">Notifications</div>
          <div v-if="!getHasNotifications(props.row)">No notifications</div>
          <template v-if="employer.notification_email">
            <div v-if="props.row.notification_email_dt">
              <q-icon name="check_circle" color="positive" size="16px"/>
              Application emailed at
              {{ dateTimeUtil.getDateTime(props.row.notification_email_dt, { isIncludeSeconds: false }) }}
              (current email is {{ employer.notification_email }})
            </div>
            <div v-if="props.row.notification_email_failure_dt">
              <q-icon name="error" color="negative" size="16px"/>
              Application email failed at
              {{ dateTimeUtil.getDateTime(props.row.notification_email_failure_dt, { isIncludeSeconds: false }) }}
              (current email is {{ employer.notification_email }})
            </div>
          </template>
          <template v-if="employer.ats_cfg">
            <div v-if="props.row.notification_ats_dt">
              <q-icon name="check_circle" color="positive" size="16px"/>
              Application sent to {{ employer.ats_cfg.name }} at
              {{ dateTimeUtil.getDateTime(props.row.notification_ats_dt, { isIncludeSeconds: false }) }}
            </div>
            <div v-if="props.row.notification_ats_failure_dt">
              <q-icon name="error" color="negative" size="16px"/>
              Application failed to sent to {{ employer.ats_cfg.name }} at
              {{ dateTimeUtil.getDateTime(props.row.notification_ats_failure_dt, { isIncludeSeconds: false }) }}
              <div>Reason: {{ props.row.notification_ats_failure_msg }}</div>
            </div>
          </template>
          <div v-if="hasApplicationFeedback(props.row)">
            <div class="text-bold q-mt-md q-mb-sm">Feedback</div>
            <div class="q-mb-sm">
              <div class="text-bold">Do you know {{ props.row.first_name }}?</div>
              <div>{{ applicantFeedbackUtil.getKnowApplicantLabel(props.row.feedback.feedback_know_applicant) }}</div>
            </div>
            <div class="q-mb-sm">
              <div class="text-bold">Would you recommend {{ props.row.first_name }} for this job?</div>
              <div>{{
                  applicantFeedbackUtil.getRecommendApplicantLabel(props.row.feedback.feedback_recommend_this_job)
                }}
              </div>
            </div>
            <div class="q-mb-sm">
              <div class="text-bold">Would you recommend {{ props.row.first_name }} for any job?</div>
              <div>{{
                  applicantFeedbackUtil.getRecommendApplicantLabel(props.row.feedback.feedback_recommend_any_job)
                }}
              </div>
            </div>
            <div class="q-mb-sm">
              <div class="text-bold">Is there any other information you want to share about {{
                  props.row.first_name
                }}?
              </div>
              <div>{{ props.row.feedback.feedback_note }}</div>
            </div>
          </div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>

import CustomTooltip from 'components/CustomTooltip.vue'
import DialogApplicantReview from 'components/dialogs/DialogApplicantReview.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import SelectLocation from 'components/inputs/SelectLocation.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import { useQuasar } from 'quasar'
import applicantFeedbackUtil from 'src/utils/applicant-feedback.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

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
  props: {
    isEmployer: Boolean
  },
  data () {
    return {
      isLoading: true,
      applications: [],
      locations: [],
      employer: {},
      applicationFilter: { ...applicationFilterTemplate },
      pagination,
      dateRange: { ...defaultDateRange },
      applicantFeedbackUtil,
      dataUtil,
      dateTimeUtil,
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
      const fields = [
        { name: 'applicant', field: 'first_name', align: 'left', label: 'Applicant', sortable: true },
        { name: 'job_title', field: 'job_title', align: 'left', label: 'Job', sortable: true },
        { name: 'locations', field: 'locations', align: 'left', label: 'Job Locations' },
        {
          name: 'recommended',
          field: (app) => app.feedback.feedback_recommend_this_job,
          align: 'left',
          label: 'Recommended',
          format: (val) => applicantFeedbackUtil.getRecommendApplicantLabel(val),
          sortable: true
        },
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
        }
      ]
      if (this.isEmployer) {
        fields.push({ name: 'referrer', field: 'owner_first_name', align: 'left', label: 'Referrer', sortable: true })
      }
      return fields
    }
  },
  methods: {
    clearApplicationFilter () {
      this.applicationFilter = { ...applicationFilterTemplate }
    },
    hasApplicationFeedback (application) {
      for (const val of Object.values(application.feedback)) {
        if (!dataUtil.isNil(val)) {
          return true
        }
      }
      return false
    },
    getIsNotificationFailure (application) {
      if (this.employer.notification_email && application.notification_email_failure_dt) {
        return true
      }
      if (this.employer.ats_cfg && application.notification_ats_failure_dt) {
        return true
      }
      return false
    },
    getHasNotifications (application) {
      return (
        (this.employer.notification_email && (application.notification_email_dt || application.notification_email_failure_dt)) ||
        (this.employer.ats_cfg && (application.notification_ats_dt || application.notification_ats_failure_dt))
      )
    },
    async removeApplicationQueryParam () {
      await this.$router.replace({ name: this.$route.name, query: dataUtil.omit(this.$route.query, ['application']) })
    },
    async openReviewDialog (application) {
      const newQueryParams = Object.assign({}, this.$route.query, { application: application.id })
      await this.$router.replace({ name: this.$route.name, query: newQueryParams })
      this.q.dialog({
        component: DialogApplicantReview,
        componentProps: { application, isEdit: this.hasApplicationFeedback(application) }
      }).onOk(async () => {
        await this.removeApplicationQueryParam()
        await this.fetchApplications({ isForceRefresh: true })
      }).onDismiss(async () => {
        await this.removeApplicationQueryParam()
      }).onCancel(async () => {
        await this.removeApplicationQueryParam()
      })
    },
    async fetchApplications (
      { pagination = this.pagination, filter = this.applicationFilter, isForceRefresh = false } = {}
    ) {
      if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
        return {}
      }
      this.isLoading = true
      const requestCfg = {
        is_raw_data: true,
        filter_by: JSON.stringify(filter),
        page_count: pagination.page,
        sort_order: pagination.sortBy,
        is_descending: pagination.descending
      }
      if (this.isEmployer) {
        requestCfg.employer_id = this.authStore.propUser.employer_id
      } else {
        requestCfg.owner_id = this.authStore.propUser.id
      }
      const paginatedApplications = await this.dataStore.getApplications(
        this.dateRange.from, this.dateRange.to, requestCfg, isForceRefresh
      )
      this.applications = paginatedApplications.applications || []
      this.locations = paginatedApplications.locations || []
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = paginatedApplications.total_application_count
      this.isLoading = false
    }
  },
  async mounted () {
    await Promise.all([
      this.fetchApplications(),
      this.employerStore.setEmployer(this.authStore.propUser.employer_id)
    ])
    this.employer = this.employerStore.getEmployer(this.authStore.propUser.employer_id)

    // Open the feedback dialog if the application ID is in the query
    // Note this won't always work because the application ID could point to an
    // application that isn't on the first page of application results
    const { application: applicationId } = this.$route.query
    const application = this.applications.find((app) => app.id === parseInt(applicationId))
    if (application) {
      await this.openReviewDialog(application)
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      dataStore: useDataStore(),
      employerStore: useEmployerStore(),
      q: useQuasar()
    }
  }
}
</script>
