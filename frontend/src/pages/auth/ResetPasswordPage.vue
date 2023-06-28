<template>
  <BaseAuthPage>
    <template v-slot:header>
      Reset password
    </template>
    <q-form
      @submit="savePassword"
      class="q-gutter-xs"
    >
      <PasswordInput v-model="password" :is-validate="true"/>
      <PasswordInput
        v-model="passwordConfirm"
        label="Confirm password"
        :custom-rules="[
          (val) => val === password || 'Password must match'
        ]"
      />
      <div>
        <q-btn
          label="Reset password"
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
import PasswordInput from 'components/inputs/PasswordInput.vue'
import BaseAuthPage from 'pages/auth/BaseAuthPage.vue'
import { useMeta } from 'quasar'
import { getAjaxFormData } from 'src/utils/requests.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'ResetPasswordPage',
  components: { PasswordInput, BaseAuthPage },
  data () {
    return {
      password: null,
      passwordConfirm: null
    }
  },
  methods: {
    goToLogin (e) {
      e.preventDefault()
      this.$router.push({ name: 'login' })
    },
    async savePassword () {
      const data = {
        password: this.password,
        uid: this.$route.params.uid,
        token: this.$route.params.token
      }
      await this.$api.put('password-reset-from-email/', getAjaxFormData(data))
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
