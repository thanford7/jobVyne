<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
          <EmployeeLeaderBoard :is-employer="false"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import EmployeeLeaderBoard from 'pages/employer/dashboard-page/EmployeeLeaderBoard.vue'

export default {
  name: 'DashboardPage',
  components: { EmployeeLeaderBoard, PageHeader }
}
</script>

<style scoped>

</style>
