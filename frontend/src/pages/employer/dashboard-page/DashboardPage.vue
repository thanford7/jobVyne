<template>
  <q-page padding>
      <div class="q-ml-sm">
        <PageHeader title="Employer dashboard"/>
        <div class="row q-mt-md">
          <div class="col-12 col-md-6 q-pa-sm">
            <LinkPerformanceChart/>
          </div>
          <div class="col-12 col-md-6 q-pa-sm">
            <DeviceTypeChart/>
          </div>
        </div>
      </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import DeviceTypeChart from 'pages/employer/dashboard-page/DeviceTypeChart.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'

export default {
  name: 'DashboardPage',
  components: { DeviceTypeChart, LinkPerformanceChart, PageHeader }
}
</script>

<style scoped>

</style>
