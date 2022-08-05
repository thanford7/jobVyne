<template>
  <q-form
    @submit="login"
  >
    <EmailInput v-model="email"/>
    <PasswordInput v-model="password"/>

    <div>
      <q-btn
        :label="(isCreate) ? createText : loginText"
        type="submit" ripple
        :style="styleOverride"
        class="w-100"
      />
    </div>
  </q-form>
</template>

<script>
import EmailInput from 'components/inputs/EmailInput.vue'
import PasswordInput from 'components/inputs/PasswordInput.vue'
import colorUtil from 'src/utils/color.js'
import formUtil from 'src/utils/form'
import { useAuthStore } from 'stores/auth-store'
import { getAjaxFormData } from 'src/utils/requests'
import { getDefaultLandingPageKey, USER_TYPES } from 'src/utils/user-types'

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
      const user = {
        email: this.email,
        password: this.password
      }
      await this.$api.post('auth/login/', getAjaxFormData(user))
      if (this.$route.name === 'login') {
        await this.authStore.setUser(true)
        const landingPageKey = getDefaultLandingPageKey(this.authStore.propUser)
        this.$router.push({ name: landingPageKey })
      } else {
        // User logged in from a dialog so redirect back to the page they were on
        this.$router.replace({ path: this.$route.fullPath, query: this.$route.query })
      }
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
