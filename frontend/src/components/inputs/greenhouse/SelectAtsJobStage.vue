<template>
  <q-select
    filled emit-value map-options
    :options="stages"
    option-value="key"
    option-label="name"
    label="Initial Candidate Stage"
    :loading="!isLoaded"
  >
    <template v-slot:after>
      <CustomTooltip :is_include_space="true">
        This is the job stage that all referred candidates will be placed into
        when they submit their applications. If not set, candidates will be placed
        in the first stage of the application process.
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import atsUtil from 'src/utils/ats.js'

export default {
  name: 'SelectAtsJobStage',
  components: { CustomTooltip },
  props: {
    ats_id: Number,
    ats_name: String
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
    this.stages = atsUtil.getFormattedStageOptions(resp.data, this.ats_name)
    this.isLoaded = true
  }
}
</script>
