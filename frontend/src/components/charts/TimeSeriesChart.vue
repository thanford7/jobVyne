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
      const props = Object.keys(chartProps).reduce((props, key) => {
        props[key] = this[key]
        return props
      }, {})
      props.labels = this.chartLabels
      const { yAxisKey, xAxisKey } = this.chartOptions.options.parsing
      // Fill in dates that don't have data
      if (props.seriesCfgs && props.seriesCfgs.length) {
        props.seriesCfgs.forEach((series) => {
          // Make sure dates are formatted correctly
          series.data.forEach((point) => {
            point[xAxisKey] = dateTimeUtil.forceToDate(point[xAxisKey])
          })
          this.chartLabels.forEach((date) => {
            if (!series.data.find((point) => point[xAxisKey] === date)) {
              series.data.push({ [xAxisKey]: date, [yAxisKey]: 0 })
            }
          })
        })
      }
      return props
    },
    chartLabels () {
      const { to, from } = this.dateRange || {}
      if (!to || !from) {
        return []
      }
      const datesInRange = dateTimeUtil.getDatesInRange(new Date(from), new Date(to))
      return dataUtil.uniqArray(datesInRange.map((date) => this.GROUPINGS[this.dateGroup].formatter(date)))
    }
  }
}
</script>
