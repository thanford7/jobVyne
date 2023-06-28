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
        props.seriesCfgs = dataUtil.deepCopy(props.seriesCfgs) // Avoid mutation
        props.seriesCfgs.forEach((series) => {
          // Make sure dates are formatted correctly
          series.data.forEach((point) => {
            point[xAxisKey] = this.GROUPINGS[this.dateGroup.toUpperCase()].formatter(point[xAxisKey])
          })

          // Add dates that don't have any data
          this.chartLabels.forEach((date) => {
            if (!series.data.find((point) => point[xAxisKey] === date)) {
              series.data.push({ [xAxisKey]: date, [yAxisKey]: 0 })
            }
          })

          // Remove data points that aren't in the date range
          series.data = series.data.reduce((validDates, dataPoint) => {
            if (this.chartLabels.includes(dataPoint[xAxisKey])) {
              validDates.push(dataPoint)
            }
            return validDates
          }, [])

          // Make sure series data is in order chart.js relies on this
          dataUtil.sortBy(series.data, xAxisKey, true)
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
      return dataUtil.uniqArray(datesInRange.map((date) => this.GROUPINGS[this.dateGroup.toUpperCase()].formatter(date)))
    }
  }
}
</script>
