<template>
  <q-page padding>
      <div class="q-ml-sm">
        <PageHeader title="Employer dashboard"/>
        <div class="row q-mt-md">
          <LinkPerformanceChart/>
        </div>
      </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'

export default {
  name: 'DashboardPage',
  components: { LinkPerformanceChart, PageHeader }
}
</script>

<style scoped>

</style>
