<template>
  <div>
    <div class="text-bold q-pb-sm border-bottom-1-gray-300">{{ chartTitle }}</div>
    <div class="q-my-sm">
      <slot name="filters"/>
    </div>
    <apexchart :type="chartType" :options="options" :series="series"/>
  </div>
</template>

<script>
import { chartProps } from 'components/charts/chartProps.js'
import dataUtil from 'src/utils/data.js'

/*
seriesCfg
{
  name: <A unique name to access this series>
  key: <Can be a string or a function to access the element for the series>
  aggFn: <Function to aggregate data points per tick>
  preGroupFn: <Optional: Function to transform data prior to grouping - use case: flattening data in an array>
  groupAttributeGetterFn: <Optional: Function to get the data attribute that will be passed to the groupFn>
  groupFn: <Function to group data points for each tick>
}
 */

export default {
  name: 'BaseChart',
  props: chartProps,
  data () {
    return {
      defaultChartOptions: {
        chart: { toolbar: { show: false } },
        plotOptions: {
          bar: {
            borderRadius: 6,
            dataLabels: {
              position: 'top'
            }
          }
        }
      }
    }
  },
  computed: {
    /**
     * Compute meta data for each series that can be used for drilldown purposes
     */
    seriesAll () {
      const series = {}
      const data = (this.filterFn) ? this.rawData.filter(this.filterFn) : this.rawData
      this.seriesCfgs.forEach((cfg) => {
        let tickData = (dataUtil.isString(cfg.key)) ? data.map((d) => d[cfg.key]) : data.map((d) => cfg.key(d))
        if (cfg.preGroupFn) {
          tickData = cfg.preGroupFn(tickData)
        }
        const getterFn = (cfg.groupAttributeGetterFn) ? cfg.groupAttributeGetterFn : (x) => x
        tickData = dataUtil.groupBy(tickData, (dataPoint) => cfg.groupFn(getterFn(dataPoint)))
        series[cfg.name] = {
          tickData,
          seriesTicks: Object.entries(tickData).reduce((seriesTicks, [tickKey, tickPoints]) => {
            seriesTicks[tickKey] = cfg.aggFn(tickPoints)
            return seriesTicks
          }, {})
        }
      })
      return series
    },
    series () {
      return Object.entries(this.seriesAll).reduce((series, [seriesName, seriesData]) => {
        const seriesTicks = seriesData.seriesTicks
        const seriesPoints = this.chartOptions.xaxis.categories.map((tickKey) => {
          return seriesTicks[tickKey] || 0
        })
        series.push({ name: seriesName, data: seriesPoints })
        return series
      }, [])
    },
    options () {
      return dataUtil.mergeDeep({}, this.defaultChartOptions, this.chartOptions)
    }
  }
}
</script>
