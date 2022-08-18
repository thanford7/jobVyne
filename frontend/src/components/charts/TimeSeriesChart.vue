<template>
  <BaseChart v-bind="passThroughProps">
    <template v-slot:appendTitle>
      <slot name="appendTitle"/>
    </template>
    <template v-slot:filters>
      <div class="flex justify-center q-mt-sm">
        <q-btn-toggle
          :model-value="dateGroup"
          @update:model-value="$emit('update:dateGroup', $event)"
          rounded unelevated
          color="grey-5"
          toggle-color="grey-8"
          :options="[
            { label: 'Day', value: GROUPINGS.DAY.key },
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
import { chartProps } from 'components/charts/chartProps.js'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'

const defaultDateRange = {
  from: dateTimeUtil.addDays(new Date(), -6, true),
  to: new Date()
}

export default {
  name: 'TimeSeriesChart',
  props: {
    defaultDateRange: {
      type: [Object, null],
      default: () => ({ ...defaultDateRange })
    },
    dateGroup: {
      type: String
    },
    ...chartProps
  },
  components: { BaseChart },
  data () {
    return {
      GROUPINGS
    }
  },
  computed: {
    passThroughProps () {
      return Object.keys(chartProps).reduce((props, key) => {
        let val = this[key]
        if (key === 'chartOptions') {
          val = this.updatedChartOptions
        }
        props[key] = val
        return props
      }, {})
    },
    updatedChartOptions () {
      const { to, from } = this.dateRange || {}
      let categories
      if (!to || !from) {
        categories = []
      } else {
        const datesInRange = dateTimeUtil.getDatesInRange(new Date(from), new Date(to))
        categories = dataUtil.uniqArray(datesInRange.map((date) => this.GROUPINGS[this.dateGroup].formatter(date)))
      }
      return dataUtil.mergeDeep({}, this.chartOptions, {
        xaxis: {
          categories
        }
      })
    }
  }
}
</script>
