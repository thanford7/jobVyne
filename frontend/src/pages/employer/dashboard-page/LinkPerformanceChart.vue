<template>
  <div v-if="isLoaded">
    <TimeSeriesChart
      chart-type="bar"
      chart-title="Submitted applications"
      :raw-data="socialLinks"
      :series-cfgs="seriesCfgs"
      :chart-options="chartOptions"
    />
  </div>
</template>

<script>
import TimeSeriesChart from 'components/charts/TimeSeriesChart.vue'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'LinkPerformanceChart',
  components: { TimeSeriesChart },
  data () {
    return {
      isLoaded: false,
      chartOptions: {},
      seriesCfgs: [
        {
          name: 'Applications',
          key: (link) => link.performance.applications,
          preGroupFn: (data) => data.reduce((allData, point) => {
            return allData.concat(point) // Flatten applications into a single array
          }, []),
          groupAttributeGetterFn: (application) => application.apply_dt,
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
