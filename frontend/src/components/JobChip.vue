<template>
  <div style="display: inline-block">
    <template v-if="jobs.length > condenseJobLimit">
      <CustomTooltip>
        <template v-slot:icon>
          <q-chip
            color="grey-7" text-color="white" size="md" :icon="icon" :dense="isDense"
          >
            Multiple jobs&nbsp;
            <span v-if="utilStore.isUnderBreakPoint('md')">(press to view)</span>
            <span v-else>(hover to view)</span>
          </q-chip>
        </template>
        <ul>
          <li v-for="job in jobs">
            {{ job.job_title }}
            <template v-if="job?.locations?.length">
              <span v-if="job.locations.length === 1">
                - {{ locationUtil.getFullLocation(job.locations[0]) }}
              </span>
              <span v-else>Multiple locations</span>
            </template>
          </li>
        </ul>
      </CustomTooltip>
    </template>
    <template v-else-if="jobs.length">
      <q-chip
        v-for="job in jobs"
        color="grey-7" text-color="white" size="md" :icon="icon"
        :dense="isDense"
      >
        {{ job.job_title }}
        <template v-if="job?.locations?.length">
          <span v-if="job.locations.length === 1">
            - {{ locationUtil.getFullLocation(job.locations[0]) }}
          </span>
          <span v-else>Multiple locations</span>
        </template>
      </q-chip>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import locationUtil from 'src/utils/location.js'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'JobChip',
  components: { CustomTooltip },
  props: {
    jobs: Array,
    isDense: {
      type: Boolean,
      default: false
    },
    icon: {
      type: [String, null]
    },
    // The max jobs to show before showing one chip with "Multiple jobs"
    condenseJobLimit: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
      locationUtil,
      utilStore: useUtilStore()
    }
  }
}
</script>
