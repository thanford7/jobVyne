<template>
  <div v-if="isInitLoaded">
    <TimeSeriesChart
      v-model:date-range="dateRange"
      v-model:date-group="dateGroup"
      chart-type="bar"
      chart-title="Submitted Applications and Page Views"
      :labels="chartLabels"
      :series-cfgs="seriesCfgs"
      :chart-options="chartOptions"
      :is-loading="isLoading"
    >
      <template v-slot:appendTitle>
        <CustomTooltip icon_size="16px">
          A page view is anytime someone visits a jobs page from an employee's link
        </CustomTooltip>
      </template>
    </TimeSeriesChart>
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import chartUtil, { chartColors } from 'components/charts/chartUtil.js'
import ChartSkeleton from 'components/charts/ChartSkeleton.vue'
import TimeSeriesChart from 'components/charts/TimeSeriesChart.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useDataStore } from 'stores/data-store.js'

export default {
  name: 'LinkPerformanceChart',
  props: {
    isEmployer: {
      type: Boolean,
      default: false
    },
    defaultDateRange: [Object, null]
  },
  components: { ChartSkeleton, CustomTooltip, TimeSeriesChart },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      chartLabels: [],
      seriesCfgs: [],
      dateRange: this.defaultDateRange || {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      },
      dateGroup: GROUPINGS.DATE.key
    }
  },
  computed: {
    chartOptions () {
      return {
        options: {
          parsing: {
            yAxisKey: 'count',
            xAxisKey: this.dateGroup
          }
        }
      }
    }
  },
  watch: {
    dateRange () {
      this.setChartRawData()
    },
    dateGroup () {
      this.setChartRawData()
    }
  },
  methods: {
    async setChartRawData () {
      if (!this.dateRange || !this.dateRange.from || !this.dateRange.to) {
        return {}
      }
      this.isLoading = true
      const params = (this.isEmployer) ? { employer_id: this.authStore.propUser.employer_id } : { owner_id: this.authStore.propUser.id }
      params.group_by = JSON.stringify([this.dateGroup])
      const [applicationsByDate, pageViewsByDate] = await Promise.all([
        this.dataStore.getApplications(
          this.dateRange.from,
          this.dateRange.to,
          params
        ),
        this.dataStore.getPageViews(
          this.dateRange.from,
          this.dateRange.to,
          params
        )
      ])
      this.chartLabels = chartUtil.getDateLabels(this.dateGroup, this.dateRange)
      this.seriesCfgs = [
        {
          label: 'Applications',
          data: chartUtil.getDateSeries(applicationsByDate, this.chartLabels, this.dateGroup, this.chartOptions.options.parsing),
          backgroundColor: chartColors.colors[0]
        },
        {
          label: 'Views',
          data: chartUtil.getDateSeries(pageViewsByDate, this.chartLabels, this.dateGroup, this.chartOptions.options.parsing),
          backgroundColor: chartColors.colors[1],
          hidden: true
        }
      ]
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

<style scoped>

</style>
