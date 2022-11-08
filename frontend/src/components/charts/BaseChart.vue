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
    <div class="chart-container__chart w-100" style="height: 20vh; position: relative">
      <canvas v-if="seriesCfgs && seriesCfgs.length" :id="chartId"></canvas>
      <div v-else class="text-center text-h6 q-mt-md">No data available</div>
    </div>
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

let chartCount = 0

export default {
  name: 'BaseChart',
  components: { DateRangeSelector },
  props: chartProps,
  data () {
    return {
      chart: null
    }
  },
  watch: {
    seriesCfgs () {
      this.chart.data.datasets = this.seriesCfgs
    }
  },
  methods: {
    openDataDialog () {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: this.selectedData }
      })
    }
  },
  setup () {
    const vals = { q: useQuasar(), chartId: `chart-${chartCount}` }
    chartCount++
    return vals
  },
  mounted () {
    const ctx = document.getElementById(this.chartId)
    const data = {
      datasets: this.seriesCfgs
    }
    if (this.labels) {
      data.labels = this.labels
    }
    this.chart = this.$createChart(ctx, Object.assign({
      type: this.chartType,
      data
    }, this.chartOptions))
  }
}
</script>
