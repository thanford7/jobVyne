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
    <div :id="containerId" class="chart-container__chart w-100" style="height: 20vh; position: relative">
      <canvas :id="chartId"></canvas>
      <div v-if="!(seriesCfgs && seriesCfgs.length)" class="text-center text-h6 q-mt-md">No data available</div>
    </div>
    <q-spinner-ios
      class="chart-container__loading"
      v-if="isLoading"
      color="primary"
    />
  </div>
</template>

<script>
import DialogShowDataTable from 'components/dialogs/DialogShowDataTable.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'

let chartCount = 0

export default {
  name: 'BaseChart',
  components: { DateRangeSelector },
  props: {
    chartType: String,
    chartTitle: [String, null],
    chartOptions: {
      type: Object,
      default: () => ({})
    },
    dateRange: {
      type: Object
    },
    isIncludeDateRange: {
      type: Boolean,
      default: true
    },
    isLoading: Boolean,
    seriesCfgs: Array,
    labels: [Array, null]
  },
  data () {
    return {
      chart: null,
      chartOptionDefaults: {
        options: {
          borderRadius: {
            topLeft: 6,
            topRight: 6,
            bottomLeft: 0,
            bottomRight: 0
          }
        }
      }
    }
  },
  watch: {
    seriesCfgs: {
      handler () {
        this.createChart()
      },
      deep: true
    }
  },
  methods: {
    createChart () {
      const data = {
        datasets: this.seriesCfgs
      }
      if (this.labels) {
        data.labels = this.labels
      }

      let ctx = document.getElementById(this.chartId)
      if (this.chart) {
        ctx.remove()
        ctx = document.createElement('canvas')
        ctx.id = this.chartId
        document.getElementById(this.containerId).appendChild(ctx)
      }
      this.chart = this.$createChart(ctx, Object.assign({
        type: this.chartType,
        data
      }, dataUtil.mergeDeep(this.chartOptionDefaults, this.chartOptions)))
    },
    openDataDialog () {
      return this.q.dialog({
        component: DialogShowDataTable,
        componentProps: { data: this.selectedData }
      })
    }
  },
  setup () {
    const vals = { q: useQuasar(), chartId: `chart-${chartCount}`, containerId: `container-${chartCount}` }
    chartCount++
    return vals
  },
  mounted () {
    this.createChart()
  }
}
</script>
