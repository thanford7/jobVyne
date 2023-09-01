<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job boards"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab v-if="!isEmployerOrgType" name="subscription" label="Job Subscriptions"/>
        <q-tab name="jobBoard" label="Job Boards"/>
<!--        TODO Add employer tab back once we've converted to pagination-->
<!--        <q-tab v-if="!isEmployerOrgType" name="employer" label="Employers"/>-->
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel v-if="!isEmployerOrgType" name="subscription">
          <div class="row q-gutter-y-md">
            <div class="col-12 callout-card">
              Job subscriptions can be used to add jobs to job boards. For example, you can "subscribe" to
              all jobs with "software" in the title and then create a job board with all the jobs from this
              subscription.
            </div>
            <div class="col-12">
              <JobSubscriptionsSection :is-employer="true"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="jobBoard">
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <JobBoardTable :is-employer="true"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel v-if="!isEmployerOrgType" name="employer">
          <EmployerSection/>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import EmployerSection from 'pages/employer/jobs-page/EmployerSection.vue'
import JobBoardTable from 'pages/employer/job-boards-page/JobBoardTable.vue'
import JobSubscriptionsSection from 'pages/employer/jobs-page/JobSubscriptionsSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import employerTypeUtil from 'src/utils/employer-types.js'
import locationUtil from 'src/utils/location.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobLinksPage',
  components: { JobBoardTable, PageHeader, JobSubscriptionsSection, EmployerSection },
  data () {
    const isEmployerOrgType = employerTypeUtil.isTypeEmployer(this.employer.organization_type)
    return {
      tab: this.$route.query.tab || ((isEmployerOrgType) ? 'jobBoard' : 'subscription'),
      isEmployerOrgType,
      employerTypeUtil,
      locationUtil
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerReferralRequests(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Job boards'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
    return {
      user,
      employer: employerStore.getEmployer(authStore.propUser.employer_id),
      employerStore,
      q: useQuasar()
    }
  }
}
</script>
