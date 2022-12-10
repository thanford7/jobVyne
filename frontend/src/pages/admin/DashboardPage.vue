<template>
<q-page padding>
    <div class="q-ml-sm">
      <PageHeader title="Admin Dashboard"/>
      <div class="row q-mt-md q-gutter-y-md">
        <div class="col-12 q-gutter-sm">
          <q-btn label="Test error message" color="primary" @click="getTestMsg"/>
          <q-btn label="Test email" color="primary" @click="sendTestEmail"/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageHeader from 'components/PageHeader.vue'
import { Loading, useMeta } from 'quasar'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'DashboardPage',
  components: { PageHeader },
  methods: {
    getTestMsg () {
      this.$api.get('test/error-msg/')
    },
    sendTestEmail () {
      this.$api.post('test/email/')
    }
  },
  preFetch () {
    const authStore = useAuthStore()
    Loading.show()

    return authStore.setUser().finally(() => {
      Loading.hide()
    })
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Admin Dashboard'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
