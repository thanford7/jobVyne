<template>
  <q-page class="flex flex-center">
    <img
      alt="Quasar logo"
      src="~assets/quasar-logo-vertical.svg"
      style="width: 200px; height: 200px"
    >
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'

export default defineComponent({
  name: 'IndexPage',
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Home'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle(pageTitle)
    }
    useMeta(metaData)
  }
})
</script>
