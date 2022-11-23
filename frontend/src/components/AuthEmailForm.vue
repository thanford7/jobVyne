<template>
  <q-form
    @submit="login"
  >
    <EmailInput v-model="email"/>
    <PasswordInput v-model="password" :is-validate="isCreate"/>

    <div class="q-mt-sm">
      <q-btn
        :label="(isCreate) ? createText : loginText"
        type="submit" ripple
        :style="styleOverride"
        class="w-100 jv-login-btn"
      />
    </div>
  </q-form>
</template>

<script>
import EmailInput from 'components/inputs/EmailInput.vue'
import PasswordInput from 'components/inputs/PasswordInput.vue'
import colorUtil from 'src/utils/color.js'
import formUtil from 'src/utils/form'
import pagePermissionsUtil from 'src/utils/permissions.js'
import { useAuthStore } from 'stores/auth-store'
import { getAjaxFormData } from 'src/utils/requests'
import { USER_TYPES } from 'src/utils/user-types'

export default {
  name: 'AuthEmailForm',
  components: { EmailInput, PasswordInput },
  data () {
    return {
      createText: 'Create account',
      loginText: 'Login',
      email: null,
      password: null,
      isPwdShown: false
    }
  },
  props: {
    isCreate: { // Whether the user is creating an account or logging in
      type: Boolean,
      default: false
    },
    defaultEmail: {
      type: [String, null],
      default: null
    },
    userTypeBit: {
      type: Number,
      default: USER_TYPES.Employee
    },
    styleOverride: {
      type: Object,
      default: () => {
        const backgroundColor = colorUtil.getPaletteColor('accent')
        return { backgroundColor, color: colorUtil.getInvertedColor(backgroundColor) }
      }
    }
  },
  methods: {
    isGoodEmail: formUtil.isGoodEmail,
    async login () {
      const userData = getAjaxFormData({
        email: this.email,
        password: this.password
      })
      if (this.isCreate) {
        await this.$api.post('user/', userData)
      }
      await this.$api.post('auth/login/', userData)
      if (this.$route.name === 'login') {
        await this.authStore.setUser(true)
        this.$router.push(pagePermissionsUtil.getDefaultLandingPage(this.authStore.propUser))
      } else {
        // User logged in from a dialog so redirect back to the page they were on
        this.$router.replace({ path: this.$route.fullPath, query: this.$route.query })
      }
      this.$emit('login')
    },
    setEmail () {
      if (!this.email && this.defaultEmail) {
        this.email = this.defaultEmail
      }
    }
  },
  created () {
    this.$api.get('auth/login-set-cookie/')
  },
  setup () {
    const authStore = useAuthStore()
    return { authStore }
  },
  mounted () {
    this.setEmail()
  },
  updated () {
    this.setEmail()
  }
}
</script>

<style scoped>

</style>
