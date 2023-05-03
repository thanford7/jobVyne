<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader
        :title="(employerType === employerTypeUtil.ORG_TYPE_EMPLOYER) ? 'Jobs & Referral bonuses' : 'Job subscriptions'"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
        @click="updateTab"
      >
        <template v-if="employerType === employerTypeUtil.ORG_TYPE_EMPLOYER">
          <q-tab name="job" label="Jobs"/>
          <q-tab name="application" label="Application Questions"/>
          <q-tab name="bonus" label="Bonuses"/>
        </template>
        <template v-else>
          <q-tab name="subscription" label="Job Subscriptions"/>
          <q-tab name="employer" label="Employers"/>
        </template>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <template v-if="employerType === employerTypeUtil.ORG_TYPE_EMPLOYER">
          <q-tab-panel name="job">
            <JobsSection :is-employer="true"/>
          </q-tab-panel>
          <q-tab-panel name="application">
            <ApplicationQuestionsSection/>
          </q-tab-panel>
          <q-tab-panel name="bonus">
            <BonusesSection/>
          </q-tab-panel>
        </template>
        <template v-else>
          <q-tab-panel name="subscription">
            <JobSubscriptionsSection/>
          </q-tab-panel>
          <q-tab-panel name="employer">
            <EmployerSection/>
          </q-tab-panel>
        </template>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ApplicationQuestionsSection from 'pages/employer/jobs-page/ApplicationQuestionsSection.vue'
import BonusesSection from 'pages/employer/jobs-page/BonusesSection.vue'
import EmployerSection from 'pages/employer/jobs-page/EmployerSection.vue'
import JobsSection from 'pages/employer/jobs-page/jobs-table/JobsSection.vue'
import JobSubscriptionsSection from 'pages/employer/jobs-page/JobSubscriptionsSection.vue'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import employerTypeUtil from 'src/utils/employer-types.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsPage',
  components: { EmployerSection, ApplicationQuestionsSection, JobSubscriptionsSection, BonusesSection, JobsSection, PageHeader },
  data () {
    const employerType = employerTypeUtil.getEmployerTypeByBit(this.employer.organization_type)
    return {
      tab: this.$route.query.tab || ((employerType === employerTypeUtil.ORG_TYPE_EMPLOYER) ? 'job' : 'subscription'),
      employerType,
      employerTypeUtil
    }
  },
  methods: {
    updateTab () {
      // Need to use full path instead of updating the query because vue router doesn't pick up
      // the mutation and doesn't update the url
      const fullPath = dataUtil.getUrlWithParams({
        addParams: [{ key: 'tab', val: this.tab }],
        deleteParams: ['tab']
      })
      this.$router.push(fullPath)
    }
  },
  watch: {
    $route: {
      handler () {
        this.tab = this.$route.query.tab
      },
      deep: true
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()

    const pageTitle = 'Jobs & Referral Bonuses'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      employer: employerStore.getEmployer(authStore.propUser.employer_id)
    }
  }
}
</script>
