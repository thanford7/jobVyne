<template>
  <BaseChart v-bind="passThroughProps">
    <template v-slot:filters>
      <DateRangeSelector
        dense
        v-model="dateRange"
        placeholder="Date range"
        :is-clearable="false"
        :force-date-range="forceDateRange"
      />
      <div class="flex justify-center q-mt-sm">
        <q-btn-toggle
          v-model="grouping"
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
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

const defaultDateRange = {
  from: dateTimeUtil.addDays(new Date(), -6, true),
  to: new Date()
}

const GROUPINGS = {
  DAY: { key: 'DAY', formatter: dateTimeUtil.getShortDate.bind(dateTimeUtil) },
  WEEK: { key: 'WEEK', formatter: dateTimeUtil.getStartOfWeekDate.bind(dateTimeUtil) },
  MONTH: { key: 'MONTH', formatter: dateTimeUtil.getMonthYearFromDate.bind(dateTimeUtil) },
  YEAR: { key: 'YEAR', formatter: dateTimeUtil.getYearFromDate.bind(dateTimeUtil) }
}

export default {
  name: 'TimeSeriesChart',
  props: chartProps,
  components: { BaseChart, DateRangeSelector },
  data () {
    return {
      forceDateRange: { ...defaultDateRange },
      dateRange: { ...defaultDateRange },
      GROUPINGS,
      grouping: GROUPINGS.DAY.key
    }
  },
  computed: {
    passThroughProps () {
      return Object.keys(chartProps).reduce((props, key) => {
        let val = this[key]
        if (key === 'chartOptions') {
          val = this.updatedChartOptions
        } else if (key === 'seriesCfgs') {
          val.forEach((cfg) => {
            cfg.groupFn = GROUPINGS[this.grouping].formatter
          })
        }
        props[key] = val
        return props
      }, {})
    },
    updatedChartOptions () {
      const datesInRange = dateTimeUtil.getDatesInRange(new Date(this.dateRange.from), new Date(this.dateRange.to))
      const categories = dataUtil.uniqArray(datesInRange.map((date) => GROUPINGS[this.grouping].formatter(date)))
      return dataUtil.mergeDeep({}, this.chartOptions, {
        xaxis: {
          categories
        }
      })
    }
  }
}
</script>
