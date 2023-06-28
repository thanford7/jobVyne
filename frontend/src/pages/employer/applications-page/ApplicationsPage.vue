<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Job applications"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12">
          <ApplicationsTable :is-employer="true"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import ApplicationsTable from 'pages/employer/applications-page/ApplicationsTable.vue'
import { Loading, useMeta } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'ApplicationsPage',
  components: { ApplicationsTable, PageHeader },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Job Applications'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
