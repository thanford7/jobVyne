<template>
  <div class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">
        404
      </div>

      <div class="text-h2" style="opacity:.4">
        Oops. Nothing here...
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'

export default defineComponent({
  name: 'ErrorNotFound',
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Error'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle(pageTitle)
    }
    useMeta(metaData)
  }
})
</script>
