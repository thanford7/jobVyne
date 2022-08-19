<template>
  <div v-if="isInitLoaded">
    <BaseChart
      v-model:date-range="dateRange"
      chart-type="bar"
      chart-title="Applications By Social Platform"
      :series-cfgs="seriesCfgs"
      :is-loading="isLoading"
    />
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
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
      const platformGroups = dataUtil.groupBy(this.chartRawData.applications, 'platform_name')
      const cfgs = Object.entries(platformGroups).map(([platformName, platformData]) => {
        return {
          seriesName: 'Applications',
          name: (platformName === 'null') ? 'Unknown' : platformName,
          rawData: platformData,
          processedData: platformData.length
        }
      })
      return dataUtil.sortBy(cfgs, { key: 'processedData', direction: -1 }, true)
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
      await this.dataStore.setSocialLinkPerformance(
        this.authStore.propUser.employer_id,
        this.dateRange.from,
        this.dateRange.to
      )
      this.isLoading = false
      this.chartRawData = this.dataStore.getSocialLinkPerformance(
        this.authStore.propUser.employer_id,
        this.dateRange.from,
        this.dateRange.to
      )
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
