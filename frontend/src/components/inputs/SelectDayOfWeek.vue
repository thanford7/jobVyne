<template>
  <q-select
    ref="select"
    filled emit-value map-options :use-chips="isMulti"
    label="Day of week"
    :options="dowOptions"
    option-value="val"
    option-label="label"
  />
</template>

<script>
import { DAYS_OF_WEEK } from 'src/utils/datetime.js'

export default {
  name: 'SelectDayOfWeek',
  props: {
    isMulti: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    dowOptions () {
      return Object.entries(DAYS_OF_WEEK).map(([dowNum, dowCfg]) => {
        return { val: dowNum, label: dowCfg.name }
      })
    }
  }
}
</script>
