<template>
  <div>
    <apexchart width="500" :type="chartType" :options="chartOptions" :series="series"/>
  </div>
</template>

<script>

/*
seriesCfg
{
  name: <A unique name to access this series>
  key: <Can be a string or a function to access the element for the series>
  aggFn: <Function to aggregate data points per tick>
  preGroupFn: <Function to transform data prior to grouping - use case: flattening data in an array>
  groupFn: <Function to group data points for each tick>
}
 */

import dataUtil from 'src/utils/data.js'

export default {
  name: 'BaseChart',
  props: {
    chartType: String,
    chartOptions: Object,
    rawData: Array,
    filterFn: [Function, null], // Filters rawData
    seriesCfgs: Array
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
        tickData = dataUtil.groupBy(tickData, cfg.groupFn)
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
    }
  }
}
</script>
