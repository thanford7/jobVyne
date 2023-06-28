<template>
  <q-form
    @submit.prevent="login()"
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
      type: [Number, null]
    },
    userProps: {
      type: [Object, null]
    },
    redirectPageUrl: {
      type: [String, null]
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
      const userData = {
        email: this.email,
        password: this.password
      }
      if (this.isCreate) {
        userData.user_type_bits = this.userTypeBit
        if (this.userProps) {
          Object.assign(userData, this.userProps)
        }
        await this.$api.post('user/', getAjaxFormData(userData))
      }
      await this.$api.post('auth/login/', getAjaxFormData(userData))
      await this.authStore.setUser(true)
      if (this.$route.name === 'login') {
        await this.$router.push(
          this.redirectPageUrl || pagePermissionsUtil.getDefaultLandingPage(this.authStore.propUser)
        )
      } else {
        // User logged in from a dialog so redirect back to the page they were on
        this.$router.replace({ path: this.$route.fullPath, query: this.$route.query })
      }
      this.$global.$emit('login')
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
