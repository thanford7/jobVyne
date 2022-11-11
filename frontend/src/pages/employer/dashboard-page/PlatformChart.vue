<template>
  <div v-if="isInitLoaded">
    <BaseChart
      v-model:date-range="dateRange"
      chart-type="bar"
      chart-title="Applications By Social Platform"
      :series-cfgs="seriesCfgs"
      :chart-options="{
        options: {
          parsing: {
            xAxisKey: 'platform_name',
            yAxisKey: 'count'
          },
          plugins: {
            legend: { display: false }
          }
        }
      }"
      :is-loading="isLoading"
    />
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
import { chartColors } from 'components/charts/chartProps.js'
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

export default {
  name: 'PlatformChart',
  components: { BaseChart, ChartSkeleton },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      chartRawData: null,
      dateRange: {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      }
    }
  },
  computed: {
    seriesCfgs () {
      return [{
        backgroundColor: [chartColors.colors[0]],
        data: this.chartRawData.map((platformData) => {
          if (platformData.platform_name === 'null' || !platformData.platform_name) {
            platformData.platform_name = 'Unknown'
          }
          return platformData
        })
      }]
    }
  },
  watch: {
    dateRange () {
      this.setChartRawData()
    }
  },
  methods: {
    async setChartRawData () {
      if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
        return {}
      }
      this.isLoading = true
      this.chartRawData = await this.dataStore.getApplications(
        this.dateRange.from,
        this.dateRange.to,
        {
          employer_id: this.authStore.propUser.employer_id,
          group_by: JSON.stringify(['platform_name'])
        }
      )
      dataUtil.sortBy(this.chartRawData, { key: 'count', direction: -1 }, true)
      this.isLoading = false
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.dataStore = useDataStore()
    await this.authStore.setUser()
    await this.setChartRawData()
    this.isInitLoaded = true
  }
}
</script>
