<template>
  <BaseAuthPage>
    <template v-slot:header>
      Email verification
    </template>
    <div v-if="isShowError">
      There was an issue with this email verification link. The link may have expired. You
      can request a new verification email from <a href="/dashboard/">your dashboard</a>.
    </div>
  </BaseAuthPage>
</template>

<script>
import BaseAuthPage from 'pages/auth/BaseAuthPage.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'VerifyEmailPage',
  components: { BaseAuthPage },
  data () {
    return {
      isShowError: false
    }
  },
  async mounted () {
    const resp = await this.$api.post('verify-email/', getAjaxFormData({
      uid: this.$route.params.uid,
      token: this.$route.params.token
    }))
    if (resp.status >= 200 && resp.status < 300) {
      this.$router.push({ name: 'dashboard' })
    } else {
      this.isShowError = true
    }
  }
}
</script>
