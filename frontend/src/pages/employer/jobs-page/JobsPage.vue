<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Jobs & Referral bonuses"/>
      <q-tabs
        v-model="tab"
        dense
        class="text-grey q-mt-md"
        active-color="primary"
        indicator-color="primary"
        align="left"
        narrow-indicator
      >
        <q-tab name="bonus" label="Bonuses"/>
        <q-tab name="job" label="Jobs"/>
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="bonus">
          <BonusesSection/>
        </q-tab-panel>
        <q-tab-panel name="job">
          <JobsSection/>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import BonusesSection from 'pages/employer/jobs-page/BonusesSection.vue'
import JobsSection from 'pages/employer/jobs-page/JobsSection.vue'
import { storeToRefs } from 'pinia/dist/pinia'
import { Loading, useMeta, useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsPage',
  components: { BonusesSection, JobsSection, PageHeader },
  data () {
    return {
      tab: 'bonus'
    }
  },
  preFetch () {
    const employerStore = useEmployerStore()
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().then(() => {
      return Promise.all([
        employerStore.setEmployer(authStore.propUser.employer_id),
        employerStore.setEmployerJobs(authStore.propUser.employer_id)
      ])
    }).finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const employerStore = useEmployerStore()
    const globalStore = useGlobalStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)

    const pageTitle = 'Jobs & Referral Bonuses'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
    const q = useQuasar()

    return { employerStore, authStore, q, user }
  }
}
</script>
