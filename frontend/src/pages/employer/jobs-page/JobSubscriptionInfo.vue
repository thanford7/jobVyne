<template>
  <div>
    <template v-if="jobSubscription.filters.job_titles">
      <q-chip
      v-for="jobTitle in jobSubscription.filters.job_titles"
      dense
    >
      {{ jobTitle.name }}
    </q-chip>
    </template>
    <LocationChip :locations="jobSubscription.filters.locations" :is-dense="true"/>
    <template v-if="jobSubscription.filters.jobs?.length && jobSubscription.filters.jobs?.length > 2">
      <CustomTooltip :is_include_icon="false">
        <template v-slot:content>
          <q-chip dense color="grey-8" text-color="white" size="13px">
            Multiple jobs
          </q-chip>
        </template>
        <ul>
          <li v-for="job in jobSubscription.filters.jobs">
            {{ job.title }}
          </li>
        </ul>
      </CustomTooltip>
    </template>
    <template v-else>
      <q-chip
        v-for="job in jobSubscription.filters.jobs"
        dense color="grey-8" text-color="white" size="13px"
      >
        {{ job.title }}
      </q-chip>
    </template>
    <template v-if="jobSubscription.filters.employers?.length && jobSubscription.filters.employers?.length > 2">
      <CustomTooltip :is_include_icon="false">
        <template v-slot:content>
          <q-chip dense color="grey-8" text-color="white" size="13px">
            Multiple employers
          </q-chip>
        </template>
        <ul>
          <li v-for="employer in jobSubscription.filters.employers">
            {{ employer.name }}
          </li>
        </ul>
      </CustomTooltip>
    </template>
    <template v-else>
      <q-chip
        v-for="employer in jobSubscription.filters.employers"
        dense color="grey-8" text-color="white" size="13px"
      >
        {{ employer.name }}
      </q-chip>
    </template>
    <template v-if="jobSubscription.filters.remote_type_bit">
      <q-chip
        v-if="jobSubscription.filters.remote_type_bit === locationUtil.REMOTE_TYPE_TRUE"
        dense color="grey-8" text-color="white"
      >
        Remote only
      </q-chip>
      <q-chip
        v-else
        dense color="grey-8" text-color="white"
      >
        On-site only
      </q-chip>
    </template>
  </div>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import LocationChip from 'components/LocationChip.vue'
import locationUtil from 'src/utils/location.js'

export default {
  name: 'JobSubscriptionInfo',
  props: {
    jobSubscription: Object
  },
  components: {
    LocationChip, CustomTooltip
  },
  data () {
    return {
      locationUtil
    }
  }
}
</script>
