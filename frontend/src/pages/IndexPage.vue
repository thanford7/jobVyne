<template>
  <q-page class="flex flex-center">
    <div class="row">
      <div class="col-12">
        <h5>This will be an amazing landing page...</h5>
      </div>
    </div>
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
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
})
</script>
