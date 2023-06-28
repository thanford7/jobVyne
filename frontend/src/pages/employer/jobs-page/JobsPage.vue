<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader
        title="Jobs & Referral bonuses"/>
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
        <q-tab name="job" label="Jobs"/>
        <q-tab name="application" label="Application Questions"/>
        <q-tab name="bonus" label="Bonuses"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="job">
          <JobsSection :is-employer="true"/>
        </q-tab-panel>
        <q-tab-panel name="application">
          <ApplicationQuestionsSection/>
        </q-tab-panel>
        <q-tab-panel name="bonus">
          <BonusesSection/>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ApplicationQuestionsSection from 'pages/employer/jobs-page/ApplicationQuestionsSection.vue'
import BonusesSection from 'pages/employer/jobs-page/BonusesSection.vue'
import JobsSection from 'pages/employer/jobs-page/jobs-table/JobsSection.vue'
import { Loading, useMeta } from 'quasar'
import dataUtil from 'src/utils/data.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsPage',
  components: { ApplicationQuestionsSection, BonusesSection, JobsSection, PageHeader },
  data () {
    return {
      tab: this.$route.query.tab || 'job'
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
