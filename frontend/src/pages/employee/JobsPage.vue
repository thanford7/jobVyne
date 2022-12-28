<template>
  <q-page padding>
      <div class="q-ml-sm">
        <PageHeader title="Jobs"/>
        <JobsSection class="q-mt-md" :is-employer="false"/>
      </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import JobsSection from 'pages/employer/jobs-page/jobs-table/JobsSection.vue'
import { Loading, useMeta } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'JobsPage',
  components: { JobsSection, PageHeader },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
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
