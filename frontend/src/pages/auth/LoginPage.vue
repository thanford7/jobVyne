<template>
  <BaseAuthPage>
    <template v-slot:header>
      {{ (isNew) ? newUserHeader : currentUserHeader }}
    </template>
    <div class="q-gutter-y-md">
      <div>
        <q-btn-toggle
          v-model="isNew"
          toggle-color="grey-8" text-color="primary" class="border-1-gray-300"
          ripple spread unelevated
          :options="[
          { label: 'New User', value: true },
          { label: 'Current User', value: false }
        ]"
        />
      </div>
      <AuthAll :is-create="isNew" :redirect-page-url="$route.query?.redirectPageUrl"/>
      <div>
        Forgot password? <a href="#" @click="goToReset">Reset password</a>
      </div>
      <div class="text-small text-grey-7 q-mt-md">
        This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy">Privacy Policy</a> and
        <a href="https://policies.google.com/terms">Terms of Service</a> apply.
      </div>
    </div>
  </BaseAuthPage>
</template>

<script>
import BaseAuthPage from 'pages/auth/BaseAuthPage.vue'
import { USER_TYPES, USER_TYPE_EMPLOYEE } from 'src/utils/user-types.js'
import { useGlobalStore } from 'stores/global-store.js'
import { useMeta } from 'quasar'
import AuthAll from 'components/AuthAll.vue'

export default {
  name: 'PageName',
  components: { BaseAuthPage, AuthAll },
  data () {
    return {
      isNew: Boolean(parseInt(this.$route.query.isNew || 0)),
      newUserHeader: 'Join JobVyne!',
      currentUserHeader: 'Welcome back!',
      USER_TYPES,
      USER_TYPE_EMPLOYEE
    }
  },
  watch: {
    isNew () {
      this.$router.push({ name: this.$route.name, query: Object.assign({}, this.$route.query, { isNew: (this.isNew) ? 1 : 0 }) })
    }
  },
  methods: {
    goToReset (e) {
      e.preventDefault()
      this.$router.push({ name: 'password-reset-generate' })
    }
  },
  setup () {
    const globalStore = useGlobalStore()

    const pageTitle = 'Login'
    const metaData = {
      title: pageTitle,
      titleTemplate: globalStore.getPageTitle
    }
    useMeta(metaData)
  }
}
</script>
