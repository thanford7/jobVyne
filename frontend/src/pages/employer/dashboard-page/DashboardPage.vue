<template>
  <q-page padding>
      <div class="q-ml-sm">
        <PageHeader title="Employer dashboard"/>
        <div class="row q-mt-md q-gutter-y-md">
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <LinkPerformanceChart :is-employer="true"/>
          </div>
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <EmployeeLeaderBoard :is-employer="true"/>
          </div>
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <DeviceTypeChart/>
          </div>
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <PlatformChart/>
          </div>
          <div class="col-12">
            <ApplicationsTable/>
          </div>
        </div>
      </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ApplicationsTable from 'pages/employer/dashboard-page/ApplicationsTable.vue'
import DeviceTypeChart from 'pages/employer/dashboard-page/DeviceTypeChart.vue'
import EmployeeLeaderBoard from 'pages/employer/dashboard-page/EmployeeLeaderBoard.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'
import PlatformChart from 'pages/employer/dashboard-page/PlatformChart.vue'

export default {
  name: 'DashboardPage',
  components: { ApplicationsTable, EmployeeLeaderBoard, PlatformChart, DeviceTypeChart, LinkPerformanceChart, PageHeader }
}
</script>

<style scoped>

</style>
