<template>
  <div v-if="isInitLoaded">
    <BaseChart
      v-model:date-range="dateRange"
      chart-type="doughnut"
      chart-title="Views By Device Type"
      :series-cfgs="seriesCfgs"
      :chart-options="chartOptions"
      :labels="labels"
      :is-loading="isLoading"
    />
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
import { chartColors } from 'components/charts/chartProps.js'
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
      pageViews: null,
      dateRange: {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      },
      chartOptions: {
        options: {
          parsing: {
            key: 'count'
          }
        }
      }
    }
  },
  computed: {
    labels () {
      return this.pageViews.map((series) => (series.is_mobile) ? 'Mobile' : 'Desktop')
    },
    seriesCfgs () {
      return [{
        data: this.pageViews,
        backgroundColor: chartColors.colors.slice(0, this.pageViews.length)
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
      this.pageViews = await this.dataStore.getPageViews(
        this.dateRange.from,
        this.dateRange.to,
        {
          employer_id: this.authStore.propUser.employer_id,
          group_by: JSON.stringify(['is_mobile'])
        }
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
