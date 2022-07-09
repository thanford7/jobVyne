<template>
  <q-page padding>
    <div class="row" style="height: 75vh">
      <div class="col-12">
        <div class="text-h6">Logging in with {{ provider }}...</div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { getAjaxFormData } from 'src/utils/requests'
import dataUtil from 'src/utils/data'
import { useGlobalStore } from 'stores/global-store'
import { useMeta } from 'quasar'

export default {
  computed: {
    provider () {
      return dataUtil.capitalize(this.$route.params.provider)
    }
  },
  methods: {
    async handleOauthCallback () {
      const provider = this.$route.params.provider
      await this.$api.post(`/social/${provider}/`, getAjaxFormData({ code: this.$route.query.code }))
      this.$router.push('/dashboard')
    }
  },
  mounted () {
    this.handleOauthCallback()
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Auth'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
