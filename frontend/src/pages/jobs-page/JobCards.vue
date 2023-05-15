<template>
  <div>
    <div v-if="!jobsByEmployer.length" class="q-mb-md">
      <q-card class="q-pa-lg">
        <div class="text-h6 text-center">No current job openings</div>
      </q-card>
    </div>
    <div class="row q-gutter-y-lg">
      <div v-for="employer in jobsByEmployer" class="col-12">
        <q-card>
          <q-card-section class="border-bottom-1-gray-300">
            <div class="row justify-center">
              <div v-if="employer.employer_logo" class="col-2">
                <div class="h-100 flex items-start align-center q-my-sm q-mr-md">
                  <q-img :src="employer.employer_logo" fit="contain" style="max-height: 80px;"/>
                </div>
              </div>
              <div class="q-pl-lg" :class="(employer.employer_logo) ? 'col-10' : 'col-12'">
                <div class="h-100 flex items-center">
                  <h5>{{ employer.employer_name }}</h5>
                </div>
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <div v-for="(jobs, jobTitle) in employer.jobs" class="border-bottom-1-gray-100">
              <h6>{{ jobTitle }}</h6>
              <JobCardInfo
                v-for="job in getLimitedJobs(employer, jobs, jobTitle)"
                :id="`job-${job.id}`"
                :job="job"
                :applications="applications"
                :job-application="jobApplication"
                :employer="employer"
                @openApplication="$emit('openApplication', $event)"
              />
              <div v-if="jobs.length > sameJobLimit" class="q-py-md">
                <a
                  v-if="!showAllJobs.includes(getShowMoreJobsKey(employer, jobTitle))"
                  href="#" @click.prevent="showAllJobs.push(getShowMoreJobsKey(employer, jobTitle))"
                >
                  Show more job locations
                </a>
                <a
                  v-else
                  href="#" @click.prevent="showAllJobs = showAllJobs.filter((key) => key !== getShowMoreJobsKey(employer, jobTitle))"
                >
                  Show fewer job locations
                </a>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import JobCardInfo from 'pages/jobs-page/JobCardInfo.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import employerStyleUtil from 'src/utils/employer-styles.js'
import formUtil from 'src/utils/form.js'

export default {
  name: 'JobCards',
  props: {
    employer: Object,
    jobsByEmployer: Object,
    applications: Array,
    jobApplication: [Object, null],
    hasJobSubscription: Boolean,
    jobPagesCount: Number
  },
  components: {
    JobCardInfo
  },
  data () {
    return {
      showAllJobs: [], // Track which jobs have been expanded
      sameJobLimit: 2,
      pageNumber: 1,
      dataUtil,
      dateTimeUtil,
      employerStyleUtil,
      formUtil
    }
  },
  computed: {
    hasNoJobs () {
      return dataUtil.isEmpty(this.jobsByEmployer)
    },
    isSingleEmployer () {
      return this.jobsByEmployer.length === 1
    }
  },
  methods: {
    getLimitedJobs (employer, jobs, jobTitle) {
      if (this.showAllJobs.includes(this.getShowMoreJobsKey(employer, jobTitle))) {
        return jobs
      }
      return jobs.slice(0, this.sameJobLimit)
    },
    getShowMoreJobsKey (employer, jobTitle) {
      return `${employer.employer_id}-${jobTitle}`
    }
  }
}
</script>
