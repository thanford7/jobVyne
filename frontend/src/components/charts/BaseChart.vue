<template>
  <div class="chart-container">
    <div class="text-bold q-pb-sm border-bottom-1-gray-300">
      {{ chartTitle }}
      <slot name="appendTitle"/>
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
      @dblclick="openDataDialog"
      @dataPointSelection="setSelectedData"
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
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import { useQuasar } from 'quasar'
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
      selectedData: null,
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
      this.labels = [] // Reset labels
      return this.seriesCfgs.reduce((series, seriesCfg) => {
        if (this.isFlatChartType) {
          this.labels.push(seriesCfg.name)
          series.push(seriesCfg.processedData)
          return series
        }

        // This is for categorical charts (e.g. bar charts)
        if (!this.chartOptions?.xaxis?.categories) {
          if (!series.length) {
            series = [{ name: seriesCfg.seriesName, data: [] }]
          }
          this.labels.push(seriesCfg.name)
          series[0].data.push({ x: seriesCfg.name, y: seriesCfg.processedData })
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
    },
    isFlatChartType () {
      return this.flatChartTypes.includes(this.chartType)
    }
  },
  methods: {
    openDataDialog () {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: this.selectedData }
      })
    },
    setSelectedData (e, chartContext, config) {
      const seriesConfig = this.seriesCfgs[config.seriesIndex]
      const categories = this.chartOptions?.xaxis?.categories
      if (this.isFlatChartType) {
        this.selectedData = seriesConfig.rawData
      } else if (categories) {
        const categoryKey = categories[config.dataPointIndex]
        this.selectedData = seriesConfig.rawData[categoryKey]
      } else {
        this.selectedData = this.seriesCfgs[config.dataPointIndex].rawData
      }
    },
    toggleInitSeries () {
      this.seriesCfgs.forEach((cfg) => {
        if (cfg.isHidden) {
          this.$refs.chart.toggleSeries(cfg.name)
        }
      })
    }
  },
  setup () {
    return { q: useQuasar() }
  },
  mounted () {
    // https://github.com/apexcharts/vue3-apexcharts/issues/3
    this.$refs.chart.$nextTick(() => {
      window.dispatchEvent(new Event('resize'))
      this.toggleInitSeries()
    })
  }
}
</script>
