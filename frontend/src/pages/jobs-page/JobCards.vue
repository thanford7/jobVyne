<template>
  <div>
    <div v-if="!jobs.length" class="q-mb-md">
      <q-card class="q-pa-lg">
        <div class="text-h6 text-center">
          <span v-if="isJobsClosed">
            Job opening has been closed
          </span>
          <span v-else>
            No current job openings
          </span>
        </div>
      </q-card>
    </div>
    <div class="row q-gutter-y-lg">
      <div v-for="job in jobs" class="col-12 col-sm-6 q-px-sm">
        <q-card
          class="hover-display-parent border-hover-info h-100"
          :style="getSelectedCardStyle(job)" bordered
        >
          <div v-if="job.application"
               class="application-date q-pa-sm border-top-rounded bg-blue-1 text-grey-8 text-small">
            <q-icon name="info" color="grey-7" size="16px"/>
            <span v-if="job.application.is_external">
              You viewed this job on
            </span>
            <span v-else>
              Applied on
            </span>
            {{ dateTimeUtil.getShortDate(job.application.created_dt) }}
          </div>
          <template v-if="!isSingleEmployer">
            <q-item>
              <q-icon
                v-if="isUserFavoriteEmployer(job.employer)"
                name="star" color="orange" title="Favorite" size="24px"
                style="position: absolute; top: 0; left: 0;"
              />
              <q-item-section avatar>
                <q-avatar>
                  <q-img :src="job.employer.logo" fit="contain"/>
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label lines="1" :title="job.job_title">
                  <span class="text-bold">{{ job.job_title }}</span>
                </q-item-label>
                <q-item-label caption>
                  <span class="text-bold">{{ job.employer.name }}</span>
                  &nbsp;<a :href="`/co/${job.employer.key}`" target="_blank">View all jobs</a>
                </q-item-label>
              </q-item-section>
            </q-item>
            <div class="text-small q-py-sm q-mx-lg">
              <div class="text-small flex items-center">
                <a v-if="job.employer.website" :href="`https://www.${job.employer.website}`" target="_blank">Website</a>
                <template v-if="job.employer.ats_name">
                  <CustomTooltip :is_include_icon="false">
                    <template v-slot:icon>
                      <q-chip size="12px" color="gray-8" dense outline>{{ job.employer.ats_name }}</q-chip>
                    </template>
                    This is the Applicant Tracking System (ATS) that {{ job.employer.name }} uses. Some ATSs are easier
                    to
                    use
                    compared with others. If you've been job searching for a bit of time, you'll know which ones 😆
                  </CustomTooltip>
                </template>
              </div>
              <!--              <div class="q-my-xs">-->
              <!--                <q-chip v-if="job.employer.industry" icon="factory" size="12px" color="gray-8" title="industry">-->
              <!--                  {{ job.employer.industry }}-->
              <!--                </q-chip>-->
              <!--                <q-chip v-if="job.employer.employee_count_min" icon="groups" size="12px" color="gray-8" title="industry">-->
              <!--                  {{ job.employer.employee_count_min }} - {{ job.employer.employee_count_max }}-->
              <!--                </q-chip>-->
              <!--              </div>-->
              <div>
                {{ job.employer.description }}
              </div>
            </div>
          </template>
          <q-item v-else>
            <q-item-section>
              <q-item-label lines="1" :title="job.job_title">
                <span class="text-bold">{{ job.job_title }}</span>
              </q-item-label>
            </q-item-section>
          </q-item>

          <q-separator/>
          <div class="row">
            <div :class="(user?.id) ? 'col-10' : 'col-12'" class="q-pa-sm">
              <q-chip :color="getPostedTimeColor(job)" size="md" icon="today">
                Posted {{ dateTimeUtil.getSmartDateDifference(dateTimeUtil.now(), job.open_date) }}
              </q-chip>
              <q-chip v-if="job.close_date" color="warning" size="md" icon="today">
                Closes on: {{ dateTimeUtil.getShortDate(job.close_date) }}
              </q-chip>
              <LocationChip :locations="job.locations" icon="place" style="max-width: 95%"/>
              <q-chip v-if="job.is_remote" color="grey-7" text-color="white" size="md" icon="laptop">
                Remote
              </q-chip>
              <q-chip color="grey-7" text-color="white" size="md" icon="schedule">
                {{ job.employment_type }}
              </q-chip>
              <q-chip v-if="dataUtil.getSalaryRange(job.salary_floor, job.salary_ceiling)" color="grey-7"
                      text-color="white" size="md" icon="attach_money">
                {{ dataUtil.getSalaryRange(job.salary_floor, job.salary_ceiling, job.salary_interval) }}
              </q-chip>
            </div>

            <template v-if="user?.id">
              <div class="col-2 border-left-1-gray-100 q-pa-sm">
                <div class="flex items-center justify-center hover-display">
                  <CustomTooltip v-if="!isUserFavoriteEmployer(job.employer)" :is_include_icon="false">
                    <template v-slot:content>
                      <q-btn icon="star" round outline dense size="12px" color="orange"
                             @click="addFavoriteEmployer(job.employer.id)"/>
                    </template>
                    Favorite {{ job.employer.name }} to easily access it from your favorites menu
                  </CustomTooltip>
                  <CustomTooltip v-else :is_include_icon="false">
                    <template v-slot:content>
                      <q-btn icon="fas fa-store-slash" round outline dense size="12px" color="negative"
                             @click="removeFavoriteEmployer(job.employer.id)"/>
                    </template>
                    Remove {{ job.employer.name }} from your favorites
                  </CustomTooltip>
                </div>
              </div>
            </template>
            <div class="col-12 border-top-1-gray-100 q-pt-sm q-px-sm">
              <q-btn
                ripple
                label="Show job details"
                color="grey-5" text-color="black" size="md"
                @click.prevent="openJobDetailsDialog(job)" class="q-mr-sm q-mb-sm"
              />
              <template v-if="!job.application || job.application.is_external">
                <q-btn
                  v-if="!job.is_use_job_url"
                  ripple
                  class="jv-apply-btn q-mb-sm" label="Apply" size="md"
                  :style="employerStyleUtil.getButtonStyle(employer)"
                  @click.prevent.stop="$emit('openApplication', job.id)"
                />
                <template v-else>
                  <q-btn
                    label="Apply on employer site"
                    ripple
                    class="jv-apply-btn q-mb-sm" icon="launch" size="md"
                    :style="employerStyleUtil.getButtonStyle(employer)"
                    @click.prevent="saveExternalApplication(job)"
                  />
                </template>
              </template>
            </div>
            <div v-if="job.general_connections?.length || job.user_connections?.length|| job.own_connection"
                 class="col-12 border-top-1-gray-100 q-py-sm q-px-md">
              <div class="text-bold q-mb-sm flex">
                <CustomTooltip :is_include_icon="false">
                  <template v-slot:content>Job Connections</template>
                  You are 700% more likely to land a job interview if you are referred by an employee. Use your
                  connections
                  to get a warm intro! 🔥
                </CustomTooltip>
                <q-space/>
                <q-btn @click="openConnectionsDialog(job)" size="sm" color="grey-8">
                  <CustomTooltip v-if="!isLoggedIn" :is_include_icon="false">
                    <template v-slot:content>
                      <q-icon name="lock"/>
                    </template>
                    You must login or create an account to view connections
                  </CustomTooltip>
                  &nbsp;&nbsp;View
                </q-btn>
              </div>
              <ul class="text-small">
                <template v-if="job.own_connection">
                  <li v-if="communityUtil.isConnectionHiringMember(job.own_connection)">
                    You are part of the hiring team for this job
                  </li>
                  <li v-else-if="communityUtil.isConnectionCurrentEmployee(job.own_connection)">
                    You work at this company
                  </li>
                  <li v-else-if="communityUtil.isConnectionFormerEmployee(job.own_connection)">
                    You previously worked at this company
                  </li>
                </template>
                <li v-for="connection in job.user_connections">
                  {{ getUserConnectionLabel(connection) }}
                </li>
                <li v-for="connection in job.general_connections">
                  {{ getGeneralConnectionLabel(connection) }}
                </li>
              </ul>
            </div>
          </div>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogJobRequirements from 'components/dialogs/DialogJobRequirements.vue'
import DialogLogin from 'components/dialogs/DialogLogin.vue'
import DialogShowEmployerConnections from 'components/dialogs/DialogShowEmployerConnections.vue'
import LocationChip from 'components/LocationChip.vue'
import { useQuasar } from 'quasar'
import colorUtil from 'src/utils/color.js'
import communityUtil from 'src/utils/community.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import formUtil from 'src/utils/form.js'
import { getAjaxFormData, openUrlInNewTab } from 'src/utils/requests.js'
import { USER_TYPE_CANDIDATE, USER_TYPES } from 'src/utils/user-types.js'

export default {
  name: 'JobCards',
  props: {
    user: [Object, null],
    employer: [Object, null],
    userFavorites: Object,
    jobs: Object,
    isSingleEmployer: Boolean,
    isJobsClosed: Boolean,
    jobApplication: [Object, null],
    jobPagesCount: Number
  },
  components: {
    LocationChip,
    CustomTooltip
  },
  data () {
    return {
      pageNumber: 1,
      communityUtil,
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      formUtil,
      q: useQuasar(),
      openUrlInNewTab
    }
  },
  computed: {
    isLoggedIn () {
      return this.user && !dataUtil.isEmpty(this.user)
    }
  },
  methods: {
    getUserConnectionLabel (connection) {
      let connectionLabel = dataUtil.pluralize('connection', connection.count)
      const workLabel = (connection.count === 1) ? 'works' : 'work'
      if (connection.type === 'same_profession') {
        connectionLabel += ` who ${workLabel} in this department`
      } else if (connection.type === 'ta_profession') {
        connectionLabel += ` who ${workLabel} in the hiring department`
      } else {
        connectionLabel += ` who ${workLabel} in a different department`
      }
      return connectionLabel
    },
    getGeneralConnectionLabel (connection) {
      let connectionLabel = dataUtil.pluralize('connection', connection.connection_count)
      if (communityUtil.isConnectionHiringMember(connection.connection_type)) {
        connectionLabel += (connection.connection_count === 1) ? ' is' : ' are'
        connectionLabel += ' hiring for this job'
      } else if (communityUtil.isConnectionCurrentEmployee(connection.connection_type)) {
        connectionLabel += (connection.connection_count === 1) ? ' works' : ' work'
        connectionLabel += ' at this company'
      } else if (communityUtil.isConnectionFormerEmployee(connection.connection_type)) {
        connectionLabel += ' used to work at this company'
      } else if (communityUtil.isConnectionKnowEmployee(connection.connection_type)) {
        connectionLabel += (connection.connection_count === 1) ? ' knows' : ' know'
        connectionLabel += ' someone who works at this company'
      }
      return connectionLabel
    },
    isUserFavoriteEmployer (employer) {
      if (!this.userFavorites?.employers) {
        return false
      }
      return Boolean(
        this.userFavorites?.employers.find((favoriteEmployer) => favoriteEmployer.employer_id === employer.id)
      )
    },
    openConnectionsDialog (job) {
      if (!this.isLoggedIn) {
        return this.q.dialog({
          component: DialogLogin,
          componentProps: {
            redirectPageUrl: window.location.pathname,
            redirectParams: dataUtil.getQueryParams(),
            userTypeBit: USER_TYPES[USER_TYPE_CANDIDATE]
          }
        })
      }
      return this.q.dialog({
        component: DialogShowEmployerConnections,
        componentProps: { job }
      })
    },
    async addFavoriteEmployer (employerId) {
      await this.$api.post('user/favorite/', getAjaxFormData({
        employer_id: employerId
      }))
      this.$emit('updateUserFavorites')
    },
    async removeFavoriteEmployer (employerId) {
      await this.$api.delete('user/favorite/', {
        data: getAjaxFormData({ employer_id: employerId, user_id: this.user.id })
      })
      this.$emit('updateUserFavorites')
    },
    async saveExternalApplication (job) {
      if (!this.user?.id) {
        this.$emit('userSignup', { id: job.id, application_url: job.application_url })
        return
      }
      const jobUrl = dataUtil.getUrlWithParams({
        isExcludeExistingParams: false,
        addParams: [{ key: 'utm_source', val: 'jobvyne' }, { key: 'ref', val: 'jobvyne' }],
        path: job.application_url
      })
      window.open(jobUrl, '_blank')
      await this.$api.post('job-application/external/', getAjaxFormData({
        job_id: job.id,
        filter_id: this.$route.params.filterId,
        referrer_user_id: this.$route?.query?.connect,
        referrer_employer_key: this.$route?.params?.employerKey,
        professionKey: this.$route.params.professionKey,
        platform_name: this.$route?.query?.platform
      }))
      this.$emit('updateApplications')
    },
    openJobDetailsDialog (job) {
      this.q.dialog({
        component: DialogJobRequirements,
        componentProps: { job }
      })
    },
    getHeaderStyle () {
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return {
        backgroundColor: primaryColor,
        color: colorUtil.getInvertedColor(primaryColor)
      }
    },
    getSelectedCardStyle (job) {
      if (!this.jobApplication || this.jobApplication.id !== job.id) {
        return {}
      }
      const primaryColor = colorUtil.getEmployerPrimaryColor(this.employer)
      return {
        boxShadow: `0 0 5px 2px ${primaryColor}`
      }
    },
    getPostedTimeColor (job) {
      const daysDiff = dateTimeUtil.getDateDifference(job.open_date, dateTimeUtil.now())
      if (daysDiff > 60) {
        return 'negative'
      } else if (daysDiff > 30) {
        return 'warning'
      } else {
        return 'positive'
      }
    }
  },
  async mounted () {
    if (this.user?.id && this.$route.query?.application_url) {
      await this.saveExternalApplication({
        application_url: this.$route.query?.application_url,
        id: this.$route.query?.id
      })
      const query = dataUtil.omit(this.$route.query, ['application_url', 'id'])
      await this.$router.replace({ query })
      const fullPath = dataUtil.getUrlWithParams({ deleteParams: ['application_url', 'id'] })
      window.history.replaceState({ path: fullPath }, '', fullPath)
    }
  }
}
</script>
