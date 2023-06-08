<template>
  <div>
    <div v-if="getJobApplication(job.id)" class="application-date q-pa-sm border-top-rounded" :style="getHeaderStyle()">
      <span v-if="getJobApplication(job.id).is_external_application">
        You viewed this job on
      </span>
      <span v-else>
        Applied on
      </span>
      {{ dateTimeUtil.getShortDate(getJobApplication(job.id).created_dt) }}
    </div>
    <div
      :style="getSelectedCardStyle(job)"
      class="jv-job-card bg-hover-gray-100 q-pa-sm"
    >
      <div class="text-grey-7 q-mb-sm">
        Posted on: {{ dateTimeUtil.getShortDate(job.open_date) }}
        <span v-if="job.close_date">| Closes on: {{ dateTimeUtil.getShortDate(job.close_date) }}</span>
      </div>
      <LocationChip :locations="job.locations" icon="place" style="display: inline-block"/>
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
      <div class="q-gutter-sm q-pt-md q-pb-sm">
        <q-btn
          ripple
          label="Show job description"
          color="grey-5"
          text-color="black"
          @click.prevent="openJobDescriptionDialog(job)"
        />
        <template v-if="!getJobApplication(job.id) || getJobApplication(job.id).is_external_application">
          <q-btn
            v-if="!job.is_use_job_url"
            ripple
            class="jv-apply-btn"
            label="Apply"
            :style="employerStyleUtil.getButtonStyle(employer)"
            @click.prevent="$emit('openApplication', job.id)"
          />
          <template v-else>
            <q-btn
              ripple
              class="jv-apply-btn" icon="launch" label="Apply on employer site"
              :style="employerStyleUtil.getButtonStyle(employer)"
              @click.prevent="saveExternalApplication(job)"
            />
          </template>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import DialogShowText from 'components/dialogs/DialogShowText.vue'
import LocationChip from 'components/LocationChip.vue'
import { useQuasar } from 'quasar'
import colorUtil from 'src/utils/color.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import formUtil from 'src/utils/form.js'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'JobCardInfo',
  props: {
    job: Object,
    employer: Object,
    applications: Array,
    jobApplication: [Object, null]
  },
  components: {
    LocationChip
  },
  data () {
    return {
      q: useQuasar(),
      dataUtil,
      dateTimeUtil,
      employerStyleUtil
    }
  },
  methods: {
    async saveExternalApplication (job) {
      const jobUrl = dataUtil.getUrlWithParams({
        isExcludeExistingParams: false,
        addParams: [{ key: 'utm_source', val: 'jobvyne' }],
        path: job.application_url
      })
      window.open(jobUrl, '_blank')
      await this.$api.post('job-application/external/', getAjaxFormData({
        job_id: job.id,
        filter_id: this.$route.params.filterId,
        platform_name: this.$route?.query?.platform
      }))
      this.$emit('updateJobs', this.pageNumber)
    },
    getJobApplication (jobId) {
      if (!this.applications) {
        return null
      }
      return this.applications.find((app) => app.employer_job.id === jobId)
    },
    openJobDescriptionDialog (job) {
      this.q.dialog({
        component: DialogShowText,
        componentProps: {
          isHtml: true,
          text: formUtil.sanitizeHtml(job.job_description),
          title: `Job description: ${job.job_title}`
        }
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
    }
  }
}
</script>
