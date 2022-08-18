<template>
  <div class="chart-container">
    <div class="text-bold q-pb-sm border-bottom-1-gray-300">
      {{ chartTitle }}<slot name="appendTitle"/>
    </div>
    <div class="q-my-sm">
      <DateRangeSelector
        v-if="isIncludeDateRange"
        dense
        :model-value="dateRange"
        @update:model-value="$emit('update:dateRange', $event)"
        placeholder="Date range"
        :is-clearable="false"
      />
      <slot name="filters"/>
    </div>
    <apexchart
      ref="chart"
      :type="chartType"
      :options="options"
      :series="series"
      @mounted="toggleInitSeries"
    />
    <q-spinner-ios
      class="chart-container__loading"
      v-if="isLoading"
      color="primary"
    />
  </div>
</template>

<script>
/* eslint-disable vue/no-side-effects-in-computed-properties */
import { chartProps } from 'components/charts/chartProps.js'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import dataUtil from 'src/utils/data.js'

/*
seriesCfg
{
  name: <A unique name to access this series>
  rawData: <Array of data points used to calculate each processed data point>
  processedData: <Array of data for each tick on the graph>
}
 */

export default {
  name: 'BaseChart',
  components: { DateRangeSelector },
  props: chartProps,
  data () {
    return {
      flatChartTypes: ['pie', 'donut'],
      labels: [],
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
    series () {
      // A flat chart only has one series which is an array and each value represents a different category
      // A non-flat chart has one or more series where each series represents one or more data points within a category
      const isFlatChartType = this.flatChartTypes.includes(this.chartType)
      this.labels = [] // Reset labels
      return this.seriesCfgs.reduce((series, seriesCfg) => {
        if (isFlatChartType) {
          this.labels.push(seriesCfg.name)
          series.push(seriesCfg.processedData)
          return series
        }
        const seriesPoints = this.chartOptions.xaxis.categories.map((tickKey) => {
          return seriesCfg.processedData[tickKey] || 0
        })
        series.push({ name: seriesCfg.name, data: seriesPoints })
        return series
      }, [])
    },
    options () {
      return dataUtil.mergeDeep({}, this.defaultChartOptions, this.chartOptions, { labels: this.labels })
    }
  },
  methods: {
    toggleInitSeries () {
      this.seriesCfgs.forEach((cfg) => {
        if (cfg.isHidden) {
          this.$refs.chart.toggleSeries(cfg.name)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.chart-container {
  position: relative;

  &__loading {
    position: absolute;
    width: 60%;
    height: 70%;
    top: 50%;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
  }
}
</style>
