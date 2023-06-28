<template>
  <BaseAuthPage>
    <template v-slot:header>
      Reset password
    </template>
    <q-form
      @submit="sendPasswordReset"
      class="q-gutter-xs"
    >
      <EmailInput v-model="email"/>

      <div>
        <q-btn
          label="Send reset email"
          type="submit" ripple
          color="accent"
          class="w-100"
        />
      </div>
    </q-form>
    <div class="q-mt-md">
      <a href="#" @click="goToLogin">Back to login</a>
    </div>
  </BaseAuthPage>
</template>

<script>
import EmailInput from 'components/inputs/EmailInput.vue'
import BaseAuthPage from 'pages/auth/BaseAuthPage.vue'
import { useMeta } from 'quasar'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'GenerateResetPasswordPage',
  components: { EmailInput, BaseAuthPage },
  data () {
    return {
      email: null
    }
  },
  methods: {
    goToLogin (e) {
      e.preventDefault()
      this.$router.push({ name: 'login' })
    },
    async sendPasswordReset () {
      await this.$api.post('password-reset-generate/', getAjaxFormData({ email: this.email }))
      this.$router.push({ name: 'login' })
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Reset password'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
