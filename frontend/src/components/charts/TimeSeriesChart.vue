<template>
  <BaseChart
    @update:dateRange="$emit('update:dateRange', $event)"
  >
    <template v-slot:appendTitle>
      <slot name="appendTitle"/>
    </template>
    <template v-slot:filters>
      <div class="flex justify-center q-mt-sm">
        <q-btn-toggle
          :model-value="dateGroup"
          @update:model-value="$emit('update:dateGroup', $event)"
          rounded unelevated size="12px"
          color="grey-5"
          text-color="black"
          toggle-color="grey-8"
          :options="[
            { label: 'Day', value: GROUPINGS.DATE.key },
            { label: 'Week', value: GROUPINGS.WEEK.key },
            { label: 'Month', value: GROUPINGS.MONTH.key },
            { label: 'Year', value: GROUPINGS.YEAR.key },
          ]"
        />
      </div>
    </template>
  </BaseChart>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
import { GROUPINGS } from 'src/utils/datetime.js'

export default {
  name: 'TimeSeriesChart',
  props: {
    dateGroup: {
      type: String
    }
  },
  components: { BaseChart },
  data () {
    return {
      GROUPINGS
    }
  }
}
</script>
