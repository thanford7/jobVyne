<template>
  <q-page padding>
      <div v-if="isLoaded" class="q-ml-sm">
        <PageHeader :title="`${(isEmployer) ? 'Employer' : 'Group'} dashboard`"/>
        <div class="row q-mt-md q-gutter-y-md">
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <LinkPerformanceChart :is-employer="true"/>
          </div>
          <div v-if="isEmployer" class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <EmployeeLeaderBoard :is-employer="true"/>
          </div>
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <DeviceTypeChart/>
          </div>
          <div class="col-12 col-md-6 col-lg-4 q-pa-sm">
            <PlatformChart/>
          </div>
          <div class="col-12">
            <ApplicationsDataTable/>
          </div>
        </div>
      </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ApplicationsDataTable from 'pages/employer/dashboard-page/ApplicationsDataTable.vue'
import DeviceTypeChart from 'pages/employer/dashboard-page/DeviceTypeChart.vue'
import EmployeeLeaderBoard from 'pages/employer/dashboard-page/EmployeeLeaderBoard.vue'
import LinkPerformanceChart from 'pages/employer/dashboard-page/LinkPerformanceChart.vue'
import PlatformChart from 'pages/employer/dashboard-page/PlatformChart.vue'
import { Loading, useMeta } from 'quasar'
import employerTypeUtil from 'src/utils/employer-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'DashboardPage',
  components: { ApplicationsDataTable, DeviceTypeChart, EmployeeLeaderBoard, LinkPerformanceChart, PlatformChart, PageHeader },
  data () {
    return {
      isLoaded: false,
      isEmployer: true,
      authStore: useAuthStore(),
      employerStore: useEmployerStore(),
      employerTypeUtil
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
  },
  async mounted () {
    Loading.show()
    await this.authStore.setUser()
    const user = this.authStore.propUser
    await this.employerStore.setEmployer(user.employer_id)
    const employer = this.employerStore.getEmployer(user.employer_id)
    this.isEmployer = this.employerTypeUtil.isTypeEmployer(employer.organization_type)
    Loading.hide()
    this.isLoaded = true
  }
}
</script>
