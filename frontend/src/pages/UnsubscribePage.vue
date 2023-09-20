<template>
  <div class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center">
    <div>
      <div class="text-h2">
        We're sorry to see you go!
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        href="https://www.jobvyne.com"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { getAjaxFormData } from 'src/utils/requests.js'
import { defineComponent } from 'vue'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'

export default defineComponent({
  name: 'UnsubscribePage',
  async mounted () {
    const { key } = dataUtil.getQueryParams()
    await this.$api.post('unsubscribe/', getAjaxFormData({ key }))
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Unsubscribe'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
})
</script>
