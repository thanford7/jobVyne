<template>
  <q-page padding>
    <page-text> Logging in with {{ provider }}...</page-text>
  </q-page>
</template>

<script>
import { getAjaxFormData } from 'src/utils/requests'
import { useAuthStore } from 'stores/auth-store'
import dataUtil from 'src/utils/data'

export default {
  computed: {
    provider () {
      return dataUtil.capitalize(this.$route.params.provider)
    }
  },
  methods: {
    handleOauthCallback () {
      const provider = this.$route.params.provider
      this.$api
        .post(`social/${provider}/`, getAjaxFormData({ code: this.$route.query.code }))
        .then((resp) => {
          this.store.updateStatus(true)
          this.store.setUserProfile(resp.data.user_id)
          this.$router.push('/')
        })
    }
  },
  setup () {
    const store = useAuthStore()
    return { store }
  },
  mounted () {
    this.handleOauthCallback()
  }
}
</script>
