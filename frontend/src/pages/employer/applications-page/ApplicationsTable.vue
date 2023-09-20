<template>
  <div v-if="isLoaded">
    <div v-if="!isTable" class="row q-gutter-y-lg">
      <CollapsableCard title="Application filters" :is-dense="true" class="col-12">
        <template v-slot:body>
          <div class="col-12 q-pa-sm">
            <div class="row q-gutter-y-sm">
              <div class="col-12 col-md-6 q-pr-md-sm">
                <q-input filled borderless debounce="300" v-model="applicationFilter.applicantName"
                         label="Applicant name">
                  <template v-slot:append>
                    <q-icon name="search"/>
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-6 q-pl-md-sm">
                <q-input filled borderless debounce="300" v-model="applicationFilter.applicantEmail"
                         label="Applicant email">
                  <template v-slot:append>
                    <q-icon name="search"/>
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-6 q-pr-md-sm">
                <q-input filled borderless debounce="300" v-model="applicationFilter.jobTitle" label="Job title">
                  <template v-slot:append>
                    <q-icon name="search"/>
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-6 q-pl-md-sm">
                <SelectLocation v-model="applicationFilter.locations" :is-multi="true" :locations="locations"/>
              </div>
              <div class="col-12 col-md-6 q-pr-md-sm">
                <q-select
                  v-model="applicationFilter.recommended"
                  filled emit-value map-options multiple use-chips
                  :options="applicantFeedbackUtil.getRecommendApplicantOpts()"
                  option-value="val"
                  option-label="label"
                  label="Recommended by referrer"
                />
              </div>
            </div>
          </div>
          <div class="col-12 q-pa-sm">
            <div class="text-small">Sort by</div>
            <div>
              <q-btn-toggle
                v-model="pagination.sortBy"
                rounded unelevated dense
                toggle-color="primary"
                text-color="grey-5"
                class="border-1-primary"
                padding="4px 10px"
                :options="applicationSortOptions"
              >
                <template v-slot:applicant>
                  <div class="row items-center no-wrap">
                    Applicant Name
                  </div>
                </template>

                <template v-slot:job_title>
                  <div class="row items-center no-wrap">
                    Job Title
                  </div>
                </template>

                <template v-slot:created_dt>
                  <div class="row items-center no-wrap">
                    Application Date
                  </div>
                </template>

                <template v-slot:recommended>
                  <div class="row items-center no-wrap">
                    Recommended Referral
                  </div>
                </template>

                <template v-if="isEmployer" v-slot:total_user_rating>
                  <div class="row items-center no-wrap">
                    User Reviews
                  </div>
                </template>
              </q-btn-toggle>
              <q-btn-toggle
                v-model="pagination.descending"
                rounded unelevated dense
                toggle-color="primary"
                text-color="grey-5"
                class="border-1-primary"
                padding="4px 10px"
                :options="[
                  {value: true, slot: 'descending'},
                  {value: false, slot: 'ascending'},
                ]"
              >
                <template v-slot:descending>
                  <div class="row items-center no-wrap">
                    <q-icon name="arrow_downward"/>
                  </div>
                </template>

                <template v-slot:ascending>
                  <div class="row items-center no-wrap">
                    <q-icon name="arrow_upward"/>
                  </div>
                </template>
              </q-btn-toggle>
            </div>
          </div>
        </template>
      </CollapsableCard>
      <div class="col-12">
        <div v-if="isEmployer && !user.connected_emails?.length" class="callout-card">
          <q-icon name="lightbulb" color="warning" size="24px"/>
          Want to email applicants? Connect your Google account on your <a href="/account/settings?tab=connection">Account page</a>.
        </div>
        <q-tabs
          v-model="applicationFilter.application_status"
          dense
          class="text-grey-7 bg-grey-2 q-mt-md border-rounded"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab
            v-for="applicationStatus in applicationStatuses"
            :name="applicationStatus.val" :label="applicationStatus.label"
          />
        </q-tabs>
      </div>
      <div v-if="pagination.totalPageCount > 1" class="col-12">
        <q-pagination
          v-model="pagination.page"
          :max-pages="5"
          :max="pagination.totalPageCount"
          input
        />
      </div>
      <div v-if="isEmployer" class="col-12">
        <q-btn-dropdown
          v-if="user.connected_emails?.length"
          label="Bulk actions" color="primary"
          rounded unelevated dense padding="5px 10px"
          class="q-mr-sm"
        >
          <q-list>
            <q-item v-if="user.connected_emails?.length" clickable v-close-popup @click="openEmailApplicantsDialog()">
              <q-item-section avatar>
                <q-icon name="email"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>Email {{ dataUtil.pluralize('applicant', selectedApplicationIds.length) }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-btn
          unelevated dense rounded label="Select all applications" color="grey-6"
          @click="selectAllApplications"
        />
        <q-btn
          v-if="selectedApplicationIds.length"
          class="q-ml-sm"
          unelevated dense rounded label="Unselect all applications" color="grey-6"
          @click="unselectAllApplications"
        />
      </div>
      <div v-for="application in applications" class="col-12 col-md-4 col-lg-3 q-px-sm">
        <q-card class="h-100 q-pb-md">
          <div class="row" :style="employerJobTitleColors[application.job_title]">
            <div v-if="isEmployer" class="col-1">
              <q-checkbox v-model="application.isSelected"
                          @update:model-value="toggleSelectedApplication($event, application.id)"/>
            </div>
            <div class="col-11">
              <div class="q-pa-sm text-center">
                {{ application.job_title }}
                <div>
                  <LocationChip v-if="application.locations?.length" :locations="application.locations"
                                :is-dense="true"/>
                </div>
              </div>
            </div>
          </div>
          <div v-if="isEmployer" class="q-px-sm q-py-sm q-gutter-y-sm border-bottom-1-gray-300">
            <DropdownApplicationStatus
              v-model="application.application_status"
              :is-employer="isEmployer"
              @update:model-value="saveApplication(application)"
              class="w-100"
            />
            <q-btn-toggle
              v-model="application.personal_rating"
              @update:model-value="saveApplicationUserRating(application)"
              rounded unelevated dense spread
              :toggle-color="applicationUtil.RATINGS[application.personal_rating]?.color"
              text-color="grey-5"
              :options="[
                  {value: applicationUtil.POSITIVE, slot: 'positive'},
                  {value: applicationUtil.NEUTRAL, slot: 'neutral'},
                  {value: applicationUtil.NEGATIVE, slot: 'negative'}
                ]"
            >
              <template v-slot:positive>
                <div class="row items-center no-wrap">
                  <q-icon size="24px" :name="applicationUtil.RATINGS[applicationUtil.POSITIVE].icon"/>
                </div>
              </template>

              <template v-slot:neutral>
                <div class="row items-center no-wrap">
                  <q-icon size="24px" :name="applicationUtil.RATINGS[applicationUtil.NEUTRAL].icon"/>
                </div>
              </template>

              <template v-slot:negative>
                <div class="row items-center no-wrap">
                  <q-icon size="24px" :name="applicationUtil.RATINGS[applicationUtil.NEGATIVE].icon"/>
                </div>
              </template>
            </q-btn-toggle>
          </div>
          <div class="q-pa-md">
            <div class="text-bold">
              {{ application.first_name }} {{ application.last_name }}
            </div>
            <div>
              Applied {{ getAppliedDaysAgo(application) }}
            </div>
            <div class="q-mt-sm">
              <q-chip
                v-if="application.referrer"
                :label="`Referred by ${application.referrer.first_name} ${application.referrer.last_name}`"
                icon="person_add"
              />
              <q-chip
                v-if="hasApplicationFeedback(application)"
                :icon="applicantFeedbackUtil.getRecommendApplicantIcon(application.feedback.feedback_recommend_this_job)"
              >
                Recommended: {{
                  applicantFeedbackUtil.getRecommendApplicantLabel(application.feedback.feedback_recommend_this_job)
                }}
                <template v-if="application.feedback.feedback_note">
                  <CustomTooltip :is_include_icon="false">
                    <template v-slot:content>
                      &nbsp;<q-icon size="20px" color="grey-7" name="description"/>
                    </template>
                    {{ application.feedback.feedback_note }}
                  </CustomTooltip>
                </template>
              </q-chip>
            </div>
            <div class="q-mt-sm">
              <q-btn
                v-if="!isEmployer"
                size="sm" color="primary" dense
                :icon="(hasApplicationFeedback(application)) ? 'edit' : 'add'"
                :label="`${(hasApplicationFeedback(application)) ? 'Edit' : 'Add'} review `"
                @click="openReviewDialog(application)"
              />
            </div>
          </div>
          <div class="bg-grey-3 q-px-sm">Credentials</div>
          <div class="q-px-md q-gutter-y-sm q-py-sm">
            <div v-if="application.resume_url">
              <q-icon name="feed"/>&nbsp;
              <a :href="application.resume_url" target="_blank">Resume</a>
            </div>
            <div v-if="application.academic_transcript_url">
              <q-icon name="feed"/>&nbsp;
              <a :href="application.academic_transcript_url" target="_blank">Academic Transcript</a>
            </div>
            <div v-if="application.cover_letter_url">
              <q-icon name="feed"/>&nbsp;
              <a :href="application.cover_letter_url" target="_blank">Cover Letter</a>
            </div>
            <div v-if="application.linkedin_url">
              <q-icon name="fa-brands fa-linkedin"/>&nbsp;
              <a :href="application.linkedin_url" target="_blank">LinkedIn Profile</a>
            </div>
          </div>
          <template v-if="application.ratings?.length">
            <div class="bg-grey-3 q-px-sm">Reviews</div>
            <div class="q-px-md q-gutter-y-sm q-py-sm">
              <div v-for="rating in application.ratings">
                <q-icon
                  :name="applicationUtil.RATINGS[rating.rating].icon"
                  :color="applicationUtil.RATINGS[rating.rating].color"
                />
                {{ rating.user_name }}
              </div>
            </div>
          </template>
          <div class="bg-grey-3 q-px-sm">Contact</div>
          <div class="q-px-md q-gutter-y-sm q-py-sm">
            <div v-if="application.phone_number">
              <q-icon name="phone"/>&nbsp;&nbsp;{{ application.phone_number }}
            </div>
            <div v-if="application.email">
              <q-icon name="email"/>&nbsp;&nbsp;{{ application.email }}
            </div>
          </div>
          <template v-if="application.message_threads?.length">
            <div class="bg-grey-3 q-px-sm">Messages</div>
            <div class="q-px-md q-gutter-y-sm q-pt-sm">
              <div>
                <div class="text-small">Latest message</div>
                <div>
                  <q-icon
                    v-if="isMessageOutbound(application.message_threads[0][0])"
                    name="fa-solid fa-paper-plane" title="Outbound message"
                  />
                  <q-icon v-else name="fa-solid fa-reply" title="Inbound message"/>
                  &nbsp;
                  <span class="text-small text-bold">{{ application.message_threads[0][0].subject }}</span>
                </div>
                <div class="text-small">Sent: {{ dateTimeUtil.getDateTime(application.message_threads[0][0].created_dt, { isIncludeSeconds: false }) }}</div>
                <div class="text-small">{{ dataUtil.truncateText(application.message_threads[0][0].body, 100) }}</div>
                <div class="q-mt-sm">
                  <a href="#" @click.prevent="openShowEmailDialog(application)">Show all messages</a>
                </div>
              </div>
            </div>
          </template>
        </q-card>
      </div>
      <div v-if="!applications?.length" class="col-12 ">
        <q-card>
          <div class="q-pa-sm text-center text-h6">
            No applications match the current filters
          </div>
        </q-card>
      </div>
      <div v-if="pagination.totalPageCount > 1" class="col-12">
        <q-pagination
          v-model="pagination.page"
          :max-pages="5"
          :max="pagination.totalPageCount"
          input
        />
      </div>
    </div>
    <q-table
      v-else
      :loading="isApplicationsLoading"
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
            <template v-else-if="col.name === 'source'">
              {{ col.label }}
              <TableFilter filter-name="source"
                           :has-filter="dataUtil.getBoolean(applicationFilter.sourceName && applicationFilter.sourceName.length)">
                <q-input filled borderless debounce="300" v-model="applicationFilter.sourceName"
                         placeholder="Source name">
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
              v-if="!isEmployer"
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
            <template v-else-if="col.name === 'source'">
            <span v-if="props.row.owner_id">
              {{ props.row.owner_first_name }} {{ props.row.owner_last_name }}
            </span>
              <span v-else>
              {{ props.row.link_name }}
            </span>
            </template>
            <template v-else-if="col.name === 'locations'">
              <LocationChip v-if="props.row.locations?.length" :locations="props.row.locations" :is-dense="true"/>
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
            <div class="row" style="white-space: normal">
              <div class="col-12 col-md-2 q-px-sm">
                <div class="text-bold q-mb-sm border-bottom-1-gray-300">Notifications</div>
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
                    Application failed to be sent to {{ dataUtil.capitalize(employer.ats_cfg.name) }} at
                    {{ dateTimeUtil.getDateTime(props.row.notification_ats_failure_dt, { isIncludeSeconds: false }) }}
                    <div>Reason: {{ props.row.notification_ats_failure_msg }}</div>
                  </div>
                </template>
              </div>
              <div v-if="hasApplicationFeedback(props.row)" class="col-12 col-md-4 q-px-sm">
                <div class="text-bold q-mb-sm border-bottom-1-gray-300">Feedback</div>
                <div class="q-mb-sm">
                  <div class="text-bold">Do you know {{ props.row.first_name }}?</div>
                  <div>{{
                      applicantFeedbackUtil.getKnowApplicantLabel(props.row.feedback.feedback_know_applicant)
                    }}
                  </div>
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
            </div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>

import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogApplicantReview from 'components/dialogs/DialogApplicantReview.vue'
import DialogEmployerApplicantEmail from 'components/dialogs/DialogEmployerApplicantEmail.vue'
import DialogShowEmails from 'components/dialogs/DialogShowEmails.vue'
import DropdownApplicationStatus from 'components/inputs/DropdownApplicationStatus.vue'
import SelectLocation from 'components/inputs/SelectLocation.vue'
import LocationChip from 'components/LocationChip.vue'
import TableFilter from 'components/tables/TableFilter.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { useQuasar } from 'quasar'
import applicantFeedbackUtil from 'src/utils/applicant-feedback.js'
import applicationUtil from 'src/utils/application.js'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import locationUtil from 'src/utils/location.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

const applicationFilterTemplate = {
  applicantName: null,
  applicantEmail: null,
  sourceName: null,
  locations: null,
  jobTitle: null,
  recommended: null,
  application_status: applicationUtil.APPLIED
}

export default {
  name: 'ApplicationsTable',
  components: { DropdownApplicationStatus, CustomTooltip, LocationChip, TableFilter, SelectLocation, CollapsableCard },
  props: {
    isEmployer: Boolean,
    isTable: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      isApplicationsLoading: true,
      applications: [],
      locations: [],
      employer: {},
      employerJobTitleColors: {},
      applicationFilter: { ...applicationFilterTemplate },
      pagination: {
        sortBy: 'created_dt',
        descending: true,
        page: 1,
        rowsPerPage: 25,
        rowsNumber: null,
        totalPageCount: 1
      },
      selectedApplicationIds: [],
      applicantFeedbackUtil,
      applicationUtil,
      dataUtil,
      dateTimeUtil,
      locationUtil
    }
  },
  watch: {
    applicationFilter: {
      handler () {
        this.pagination.page = 1
        this.fetchApplications({ isForceRefresh: true })
      },
      deep: true
    },
    pagination: {
      handler () {
        this.fetchApplications({ isForceRefresh: true })
      },
      deep: true
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
          format: (val) => dateTimeUtil.getShortDate(val),
          sortable: true
        }
      ]
      if (this.isEmployer) {
        fields.push({ name: 'source', field: 'owner_first_name', align: 'left', label: 'Source', sortable: true })
      }
      return fields
    },
    applicationStatuses () {
      if (this.isEmployer) {
        return Object.values(this.applicationUtil.APPLICATION_STATUSES).filter((status) => status.isEmployerValue)
      }
      return Object.values(this.applicationUtil.APPLICATION_STATUSES).filter((status) => status.isCandidateValue)
    },
    applicationSortOptions () {
      const sortOptions = [
        { value: 'applicant', slot: 'applicant' },
        { value: 'job_title', slot: 'job_title' },
        { value: 'created_dt', slot: 'created_dt' },
        { value: 'recommended', slot: 'recommended' }
      ]
      if (this.isEmployer) {
        sortOptions.push({ value: 'total_user_rating', slot: 'total_user_rating' })
      }
      return sortOptions
    }
  },
  methods: {
    clearApplicationFilter () {
      this.applicationFilter = { ...applicationFilterTemplate }
    },
    getAppliedDaysAgo (application) {
      const appliedDaysAgo = dateTimeUtil.getDateDifference(application.created_dt, dateTimeUtil.now(), 'day')
      if (!appliedDaysAgo) {
        return 'today'
      }
      return `${dataUtil.pluralize('day', appliedDaysAgo)} ago`
    },
    hasApplicationFeedback (application) {
      for (const val of Object.values(application.feedback)) {
        if (!dataUtil.isNil(val)) {
          return true
        }
      }
      return false
    },
    isMessageOutbound (message) {
      if (!this.user.connected_emails?.length) {
        return false
      }
      return this.user.connected_emails.includes(message.from_address)
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
    toggleSelectedApplication (isSelected, applicationId) {
      if (isSelected && !this.selectedApplicationIds.includes(applicationId)) {
        this.selectedApplicationIds.push(applicationId)
      } else {
        this.selectedApplicationIds = this.selectedApplicationIds.filter((appId) => appId !== applicationId)
      }
    },
    selectAllApplications () {
      this.applications.forEach((app) => {
        app.isSelected = true
        if (!this.selectedApplicationIds.includes(app.id)) {
          this.selectedApplicationIds.push(app.id)
        }
      })
    },
    unselectAllApplications () {
      this.applications.forEach((app) => {
        app.isSelected = false
      })
      this.selectedApplicationIds = []
    },
    openShowEmailDialog (application) {
      this.q.dialog({
        component: DialogShowEmails,
        componentProps: {
          emailThreads: application.message_threads
        }
      })
    },
    openEmailApplicantsDialog () {
      this.q.dialog({
        component: DialogEmployerApplicantEmail,
        componentProps: {
          applicationIds: this.selectedApplicationIds,
          employerId: this.user.employer_id
        }
      }).onOk(async () => {
        await this.fetchApplications({ isForceRefresh: true })
        this.unselectAllApplications()
      })
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
    async saveApplication (application) {
      await this.$api.put('employer/job-application/', getAjaxFormData(application))
      await this.fetchApplications({ isForceRefresh: true })
    },
    async saveApplicationUserRating (application) {
      await this.$api.post('user/job-application-review/', getAjaxFormData({
        user_id: this.user.id,
        application_id: application.id,
        rating: application.personal_rating
      }))
      await this.fetchApplications({ isForceRefresh: true })
    },
    async fetchApplications (
      { pagination = this.pagination, filter = this.applicationFilter, isForceRefresh = false } = {}
    ) {
      this.isApplicationsLoading = true
      const requestCfg = {
        is_raw_data: true,
        filter_by: JSON.stringify(filter),
        page_count: pagination.page,
        rows_per_page: pagination.rowsPerPage,
        sort_order: pagination.sortBy,
        is_descending: pagination.descending
      }
      if (this.isEmployer) {
        requestCfg.employer_id = this.user.employer_id
      } else {
        requestCfg.owner_id = this.user.id
      }
      const paginatedApplications = await this.dataStore.getApplications(null, null, requestCfg, isForceRefresh)
      this.applications = paginatedApplications.applications || []
      this.applications.forEach((app) => {
        app.isSelected = this.selectedApplicationIds.includes(app.id)
      })
      this.locations = paginatedApplications.locations || []
      Object.assign(this.pagination, pagination)
      this.pagination.rowsNumber = paginatedApplications.total_application_count
      this.pagination.totalPageCount = paginatedApplications.total_page_count
      this.isApplicationsLoading = false
    }
  },
  async mounted () {
    await Promise.all([
      this.fetchApplications(),
      this.employerStore.setEmployer(this.user.employer_id),
      this.employerStore.setEmployerJobs(this.user.employer_id, { isIncludeClosed: true })
    ])
    this.employer = this.employerStore.getEmployer(this.user.employer_id)
    const employerJobs = this.employerStore.getEmployerJobs(this.user.employer_id, { isIncludeClosed: true })
    this.employerJobTitleColors = employerJobs.reduce((allJobTitles, job) => {
      const backgroundColor = colorUtil.getRandomPastelColor()
      allJobTitles[job.job_title] = { backgroundColor, color: colorUtil.getInvertedColor(backgroundColor) }
      return allJobTitles
    }, {})

    this.isLoaded = true

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
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    return {
      dataStore: useDataStore(),
      employerStore: useEmployerStore(),
      q: useQuasar(),
      user
    }
  }
}
</script>
