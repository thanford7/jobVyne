<template>
  <div v-if="isInitLoaded">
    <BaseChart
      v-model:date-range="dateRange"
      chart-type="donut"
      chart-title="Views By Device Type"
      :series-cfgs="seriesCfgs"
      :is-loading="isLoading"
    />
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import dateTimeUtil from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

export default {
  name: 'DeviceTypeChart',
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
      return [
        {
          name: 'Mobile',
          rawData: this.mobileViews,
          processedData: this.mobileViews.reduce((totalViews, g) => {
            totalViews += g.view_count
            return totalViews
          }, 0)
        },
        {
          name: 'Desktop',
          rawData: this.desktopViews,
          processedData: this.desktopViews.reduce((totalViews, g) => {
            totalViews += g.view_count
            return totalViews
          }, 0)
        }
      ]
    },
    mobileViews () {
      return this.chartRawData.views.filter((d) => d.is_mobile)
    },
    desktopViews () {
      return this.chartRawData.views.filter((d) => !d.is_mobile)
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
      this.chartRawData = await this.dataStore.getSocialLinkPerformance(
        this.dateRange.from,
        this.dateRange.to,
        { employerId: this.authStore.propUser.employer_id }
      )
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
