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
        <CustomTooltip icon_size="16px">
          A page view is anytime someone visits a jobs page from an employee's link
        </CustomTooltip>
      </template>
    </TimeSeriesChart>
  </div>
  <ChartSkeleton v-else/>
</template>

<script>
import { chartColors } from 'components/charts/chartProps.js'
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
    defaultDateRange: [Object, null],
    defaultDateGroup: [String, null]
  },
  components: { ChartSkeleton, CustomTooltip, TimeSeriesChart },
  data () {
    return {
      isInitLoaded: false,
      isLoading: false,
      dateRange: this.defaultDateRange || {
        from: dateTimeUtil.addDays(new Date(), -6, true),
        to: new Date()
      },
      dateGroup: this.defaultDateGroup || GROUPINGS.DAY.key,
      applicationsByDate: null,
      pageViewsByDate: null,
      chartOptions: {
        options: {
          parsing: {
            yAxisKey: 'count',
            xAxisKey: 'date'
          }
        }
      }
    }
  },
  computed: {
    seriesCfgs () {
      return [
        {
          label: 'Applications',
          data: this.applicationsByDate,
          backgroundColor: chartColors.colors[0]
        },
        {
          label: 'Views',
          data: this.pageViewsByDate,
          backgroundColor: chartColors.colors[1],
          hidden: true
        }
      ]
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
      const params = (this.isEmployer) ? { employerId: this.authStore.propUser.employer_id } : { userId: this.authStore.propUser.id }
      const [applicationsByDate, pageViewsByDate] = await Promise.all([
        this.dataStore.getApplications(
          this.dateRange.from,
          this.dateRange.to,
          params
        ),
        await this.dataStore.getPageViews(
          this.dateRange.from,
          this.dateRange.to,
          params
        )
      ])
      this.applicationsByDate = applicationsByDate
      this.pageViewsByDate = pageViewsByDate
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
