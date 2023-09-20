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
        @click="updateTab"
      >
        <q-tab name="subscription" label="Job Subscriptions"/>
        <q-tab name="jobBoard" label="Job Boards"/>
        <q-tab name="employer" label="Employers"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="subscription">
          <div class="row q-gutter-y-md">
            <div class="col-12 callout-card">
              Job subscriptions can be used to add jobs to job boards. For example, you can "subscribe" to
              all jobs with "software" in the title and then create a job board with all the jobs from this
              subscription.
            </div>
            <div class="col-12">
              <JobSubscriptionsSection :is-employer="false"/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="jobBoard">
          <div class="row q-gutter-y-md">
            <div class="col-12">
              <JobBoardTable/>
            </div>
          </div>
        </q-tab-panel>
        <q-tab-panel name="employer">
          <EmployerSection/>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import JobBoardTable from 'pages/employer/job-boards-page/JobBoardTable.vue'
import EmployerSection from 'pages/employer/jobs-page/EmployerSection.vue'
import JobSubscriptionsSection from 'pages/employer/jobs-page/JobSubscriptionsSection.vue'
import { useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsPage',
  components: {
    JobBoardTable,
    EmployerSection,
    JobSubscriptionsSection,
    PageHeader
  },
  data () {
    return {
      tab: 'subscription'
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
  async mounted () {
    const authStore = useAuthStore()
    await authStore.setUser()
    const { tab } = this.$route.query
    if (tab) {
      this.tab = tab
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Jobs'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
