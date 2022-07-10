<template>
  <div class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center">
    <div>
      <BannerMessage/>
      <div class="text-h2" style="opacity:.4">
        Sorry, something went wrong
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
import BannerMessage from 'components/BannerMessage.vue'

export default defineComponent({
  name: 'ErrorPage',
  components: { BannerMessage },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Error'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
})
</script>
