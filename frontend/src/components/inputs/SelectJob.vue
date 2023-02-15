<template>
  <q-select
    v-if="isLoaded"
    ref="select"
    :multiple="isMulti" :clearable="isMulti" :use-chips="isMulti"
    filled use-input map-options emit-value
    @filter="filter"
    :options="filteredJobs"
    option-value="id" option-label="job_title"
    label="Job"
    input-debounce="500"
    lazy-rules
    :rules="(isRequired) ? [
      (val) => val || 'Job is required'
    ] : null"
  >
    <template v-slot:option="{ itemProps, opt, selected, toggleOption }">
      <q-item
        v-bind="itemProps"
        :active="selected"
        class="bg-hover border-bottom-1-gray-100"
        @click="toggleOption(opt)"
      >
        <div class="row">
          <div class="col-12">
            {{ opt.job_title }}
          </div>
          <div class="col-12 text-small">
            <LocationsCell :locations="opt.locations"/>
          </div>
        </div>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import LocationsCell from 'pages/employer/jobs-page/jobs-table/LocationsCell.vue'
import locationUtil from 'src/utils/location.js'
import { useEmployerStore } from 'stores/employer-store.js'
import dataUtil from 'src/utils/data.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'SelectJob',
  components: { LocationsCell },
  props: {
    isRequired: {
      type: Boolean,
      default: false
    },
    isMulti: {
      type: Boolean,
      default: true
    },
    employerId: {
      type: [String, Number]
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: '',
      jobs: [],
      employerStore: null,
      globalStore: null,
      locationUtil
    }
  },
  computed: {
    filteredJobs () {
      if (!this.filterTxt || !this.filterTxt.length) {
        return this.jobs
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.jobs.filter((job) => job.job_title.match(filterRegex))
    }
  },
  methods: {
    filter (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.globalStore = useGlobalStore()
    this.employerStore = useEmployerStore()
    await this.employerStore.setEmployerJobs(this.employerId)
    this.jobs = this.employerStore.getEmployerJobs(this.employerId)
    dataUtil.sortBy(this.jobs, 'job_title', true)
    this.isLoaded = true
  }
}
</script>
