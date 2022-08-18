<template>
  <div v-if="isInitLoaded">
    <TimeSeriesChart
      v-model:date-range="dateRange"
      v-model:date-group="dateGroup"
      chart-type="bar"
      chart-title="Submitted Applications and Page Views"
      :series-cfgs="seriesCfgs"
      :chart-options="chartOptions"
      :is-loading="isLoading"
    >
      <template v-slot:appendTitle>
        <CustomTooltip>
          A page view is anytime someone visits a jobs page from an employee's link
        </CustomTooltip>
      </template>
    </TimeSeriesChart>
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import TimeSeriesChart from 'components/charts/TimeSeriesChart.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

export default {
  name: 'LinkPerformanceChart',
  components: { ChartSkeleton, CustomTooltip, TimeSeriesChart },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      dateRange: {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      },
      dateGroup: GROUPINGS.DAY.key,
      chartRawData: null,
      chartOptions: {}
    }
  },
  computed: {
    seriesCfgs () {
      return [
        {
          name: 'Applications',
          rawData: this.groupedApplicationData,
          processedData: this.applicationData
        },
        {
          name: 'Views',
          rawData: this.groupedViewData,
          processedData: this.viewData,
          isHidden: true
        }
      ]
    },
    groupedApplicationData () {
      const dateGroupFn = GROUPINGS[this.dateGroup].formatter
      return dataUtil.groupBy(this.chartRawData.applications, (app) => dateGroupFn(app.apply_dt))
    },
    applicationData () {
      return Object.entries(this.groupedApplicationData).reduce((processedData, [groupKey, group]) => {
        processedData[groupKey] = group.length
        return processedData
      }, {})
    },
    groupedViewData () {
      const dateGroupFn = GROUPINGS[this.dateGroup].formatter
      return dataUtil.groupBy(this.chartRawData.views, (view) => dateGroupFn(view.access_dt))
    },
    viewData () {
      return Object.entries(this.groupedViewData).reduce((processedData, [groupKey, group]) => {
        processedData[groupKey] = group.length
        return processedData
      }, {})
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

<style scoped>

</style>
