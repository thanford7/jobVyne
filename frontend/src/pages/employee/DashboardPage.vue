<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
          <LinkPerformanceChart
            :is-employer="false"
            :default-date-group="GROUPINGS.MONTH.key"
            :default-date-range="dateRange"
          />
        </div>
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
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'
import { useMeta } from 'quasar'
import dateTimeUtil, { GROUPINGS } from 'src/utils/datetime.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'DashboardPage',
  components: { LinkPerformanceChart, EmployeeLeaderBoard, PageHeader },
  data () {
    return {
      GROUPINGS,
      dateRange: {
        from: dateTimeUtil.getStartOfMonthDate(new Date(), { monthOffset: -2 }),
        to: new Date()
      }
    }
  },
  setup () {
    const globalStore = useGlobalStore()
    const pageTitle = 'Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
