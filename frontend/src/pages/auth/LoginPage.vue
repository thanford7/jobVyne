<template>
  <BaseAuthPage>
    <template v-slot:header>
      {{ (isCreate) ? newUserHeader : currentUserHeader }}
    </template>
    <AuthAll :is-create="isCreate" :redirect-page-url="$route.query?.redirectPageUrl"/>
    <div class="q-mt-md">
      <div v-if="isCreate">
        Current user? <a href="#" @click="toggleNewUser($event, 0)">Login here</a>
      </div>
      <div v-else>
        New user? <a href="#" @click="toggleNewUser($event, 1)">Sign up here</a>
      </div>
    </div>
    <div>
      Forgot password? <a href="#" @click="goToReset">Reset password</a>
    </div>
    <div class="text-small text-grey-7 q-mt-md">
      This site is protected by reCAPTCHA and the Google
      <a href="https://policies.google.com/privacy">Privacy Policy</a> and
      <a href="https://policies.google.com/terms">Terms of Service</a> apply.
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
      newUserHeader: 'Join JobVyne!',
      currentUserHeader: 'Welcome back!',
      USER_TYPES,
      USER_TYPE_EMPLOYEE
    }
  },
  computed: {
    isCreate () {
      const isNew = this.$route.query.isNew || 0
      return Boolean(parseInt(isNew))
    }
  },
  methods: {
    goToReset (e) {
      e.preventDefault()
      this.$router.push({ name: 'password-reset-generate' })
    },
    toggleNewUser (e, isNew) {
      e.preventDefault()
      this.$router.push({ name: this.$route.name, query: Object.assign({}, this.$route.query, { isNew }) })
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
