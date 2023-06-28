<template>
  <q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Dashboard"/>
    </div>
  </q-page>
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'
import { useGlobalStore } from 'stores/global-store'
import { Loading, useMeta } from 'quasar'
import PageHeader from 'components/PageHeader.vue'

export default {
  name: 'DashboardPage',
  components: { PageHeader },
  preFetch () {
    const authStore = useAuthStore()
    const employerStore = useEmployerStore()
    Loading.show()

    return authStore.setUser().then(() => {
      if (authStore.propUser.employer_id) {
        return Promise.all([
          employerStore.setEmployer(authStore.propUser.employer_id)
        ])
      }
    }).finally(() => {
      Loading.hide()
    })
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
