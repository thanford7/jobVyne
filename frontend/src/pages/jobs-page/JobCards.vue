<template>
  <div>
    <div v-if="!jobsByEmployer.length" class="q-mb-md">
      <q-card class="q-pa-lg">
        <div class="text-h6 text-center">No current job openings</div>
      </q-card>
    </div>
    <div class="row q-gutter-y-lg">
      <div v-for="employer in jobsByEmployer" class="col-12">
        <q-card :id="`employer-${employer.employer_id}`">
          <q-card-section
            v-if="!isSingleEmployer"
            class="border-bottom-1-gray-300 custom-sticky custom-sticky-1 bg-white"
          >
            <div class="row justify-center">
              <div v-if="employer.employer_logo" class="col-2">
                <div class="h-100 flex items-start align-center q-my-sm q-mr-md">
                  <q-img :src="employer.employer_logo" fit="contain" style="max-height: 80px;"/>
                </div>
              </div>
              <div class="q-pl-lg" :class="(employer.employer_logo) ? 'col-10' : 'col-12'">
                <div class="h-100 flex items-center">
                  <h5 class="w-100 q-mb-none">{{ employer.employer_name }}</h5>
                  <div>
                    <a :href="`/co/${employer.employer_key}`" target="_blank">View all jobs</a>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
          <div
            v-for="(jobsByTitle, jobDepartment) in employer.jobs"
          >
            <div
              class="text-bold bg-grey-7 text-white q-px-sm q-py-xs custom-sticky"
              :class="`custom-sticky-${(isSingleEmployer) ? '1' : '2'}`"
            >
              Department: {{ jobDepartment }}
            </div>
            <q-card-section class="q-pb-none">
              <div
                v-for="(jobs, jobTitle) in jobsByTitle"
                :id="`job-${employer.employer_id}-${jobs[0].id}`"
                class="border-bottom-1-gray-100"
              >
                <h6
                  class="bg-white custom-sticky"
                  :class="`custom-sticky-${(isSingleEmployer) ? '2' : '3'}`"
                >
                  {{ jobTitle }}
                </h6>
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
                    href="#"
                    @click.prevent="showAllJobs = showAllJobs.filter((key) => key !== getShowMoreJobsKey(employer, jobTitle))"
                  >
                    Show fewer job locations
                  </a>
                </div>
              </div>
            </q-card-section>
          </div>
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
    jobsByEmployer: Object,
    isSingleEmployer: Boolean,
    hasNoJobs: Boolean,
    applications: Array,
    jobApplication: [Object, null],
    jobPagesCount: Number,
    scrollStickStartPx: Number
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
  methods: {
    getLimitedJobs (employer, jobs, jobTitle) {
      if (this.showAllJobs.includes(this.getShowMoreJobsKey(employer, jobTitle))) {
        return jobs
      }
      return jobs.slice(0, this.sameJobLimit)
    },
    getShowMoreJobsKey (employer, jobTitle) {
      return `${employer.employer_id}-${jobTitle}`
    },
    updateStickyOffsets () {
      const stickyElements = document.querySelectorAll('.custom-sticky')
      let stickyOffsetPx
      let lastSticky1HeightPx
      let lastSticky2HeightPx
      for (const stickyEl of stickyElements) {
        if (stickyEl.classList.contains('custom-sticky-1')) {
          stickyOffsetPx = this.scrollStickStartPx
          lastSticky1HeightPx = stickyEl.offsetHeight
          stickyEl.style['z-index'] = 1003
        } else if (stickyEl.classList.contains('custom-sticky-2')) {
          stickyOffsetPx = this.scrollStickStartPx + lastSticky1HeightPx
          lastSticky2HeightPx = stickyEl.offsetHeight
          stickyEl.style['z-index'] = 1002
        } else if (stickyEl.classList.contains('custom-sticky-3')) {
          stickyOffsetPx = this.scrollStickStartPx + lastSticky1HeightPx + lastSticky2HeightPx
          stickyEl.style['z-index'] = 1001
        } else {
          stickyOffsetPx = this.scrollStickStartPx
        }
        stickyEl.style.top = `${stickyOffsetPx}px`
      }
    }
  },
  mounted () {
    this.updateStickyOffsets()
  },
  updated () {
    this.updateStickyOffsets()
  }
}
</script>
