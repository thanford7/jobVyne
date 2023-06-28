<template>
  <BaseAuthPage>
    <template v-slot:header>
      Email verification
    </template>
    <div v-if="isShowError">
      There was an issue with this email verification link. The link may have expired. You
      can request a new verification email from <a href="/user/profile/?tab=security">your profile</a>.
    </div>
  </BaseAuthPage>
</template>

<script>
import { AJAX_EVENTS } from 'boot/axios.js'
import BaseAuthPage from 'pages/auth/BaseAuthPage.vue'
import { useMeta } from 'quasar'
import { getAjaxFormData } from 'src/utils/requests.js'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'VerifyEmailPage',
  components: { BaseAuthPage },
  data () {
    return {
      isShowError: false
    }
  },
  async mounted () {
    this.$global.$on(AJAX_EVENTS.ERROR, () => {
      this.isShowError = true
    })
    const resp = await this.$api.post('verify-email/', getAjaxFormData({
      uid: this.$route.params.uid,
      token: this.$route.params.token
    }))
    if (resp.status >= 200 && resp.status < 300) {
      await this.authStore.setUser(true)
      this.$router.push(pagePermissionsUtil.getDefaultLandingPage(this.authStore.propUser))
    }
  },
  setup () {
    const authStore = useAuthStore()
    const globalStore = useGlobalStore()
    const pageTitle = 'Email Verification Page'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)

    return {
      authStore
    }
  }
}
</script>
