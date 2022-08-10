<template>
  <BaseAuthPage>
    <template v-slot:header>
      {{ (isCreate) ? newUserHeader : currentUserHeader }}
    </template>
    <AuthAll :is-create="isCreate"/>
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
      this.$router.push({ name: this.$route.name, query: { isNew } })
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

<style lang="scss" scoped>
.login-container {
  position: relative;
  height: 100vh;
  width: 100%;

  &::before {
    content: "";
    background: url('../../assets/background/connectwork.png') no-repeat center center fixed;
    background-size: cover;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    opacity: 0.2;
    overflow: hidden;
  }
}
</style>
