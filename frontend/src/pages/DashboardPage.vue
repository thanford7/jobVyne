<template>
  <q-page padding>
    <!-- content -->
  </q-page>
</template>

<script>
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'

export default {
  // name: 'PageName',
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
