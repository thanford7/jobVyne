<template>
  <q-select
    filled emit-value map-options
    :options="stages"
    option-value="name"
    option-label="name"
    label="Initial Candidate Stage"
    :loading="!isLoaded"
  >
    <template v-slot:after>
      <CustomTooltip>
        This is the job stage that all referred candidates will be placed into
        when they submit their applications. If not set, candidates will be placed
        in the first stage of the application process.
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'SelectAtsJobStage',
  components: { CustomTooltip },
  props: {
    ats_id: Number
  },
  data () {
    return {
      isLoaded: false,
      stages: []
    }
  },
  async mounted () {
    const resp = await this.$api.get('ats/stages/', {
      params: { ats_id: this.ats_id }
    })
    this.stages = dataUtil.sortBy(
      dataUtil.uniqBy(resp.data.map((s) => ({ name: s.name, priority: s.priority })), 'name'),
      'priority',
      true)
    this.isLoaded = true
  }
}
</script>
