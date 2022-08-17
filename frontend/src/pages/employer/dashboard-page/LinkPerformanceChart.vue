<template>
  <div v-if="isLoaded">
    <BaseChart
      chart-type="bar"
      :raw-data="socialLinks"
      :series-cfgs="seriesCfgs"
      :chart-options="chartOptions"
    />
  </div>
</template>

<script>
import BaseChart from 'components/charts/BaseChart.vue'
import dateTimeUtil from 'src/utils/datetime.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'LinkPerformanceChart',
  components: { BaseChart },
  data () {
    return {
      isLoaded: false,
      chartOptions: {
        xaxis: {
          // TODO: Add a date picker to select the range
          categories: dateTimeUtil.getDatesInRange(new Date(2022, 7, 1), new Date()).map((date) => {
            return dateTimeUtil.getShortDate(date)
          })
        }
      },
      seriesCfgs: [
        {
          name: 'Applications',
          key: (link) => link.performance.applications,
          preGroupFn: (data) => data.reduce((allData, point) => {
            return allData.concat(point) // Flatten applications into a single array
          }, []),
          groupFn: (application) => dateTimeUtil.getShortDate(application.apply_dt),
          aggFn: (applications) => applications.length
        }
      ]
    }
  },
  computed: {
    socialLinks () {
      return this.employerStore.getEmployerSocialLinks(this.authStore.propUser.employer_id)
    }
  },
  async mounted () {
    this.authStore = useAuthStore()
    this.employerStore = useEmployerStore()
    await this.authStore.setUser()
    await this.employerStore.setEmployerSocialLinks(this.authStore.propUser.employer_id)
    this.isLoaded = true
  }
}
</script>

<style scoped>

</style>
