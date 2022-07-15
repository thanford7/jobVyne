<template>
  <q-form
    @submit="login"
    class="q-gutter-xs"
  >
    <q-input
      filled
      v-model="email"
      label="Email *"
      lazy-rules
      :rules="[ val => val && val.length > 0 && isGoodEmail(val) || 'Please enter a valid email']"
    />

    <q-input
      v-model="password"
      filled
      :type="isPwdShown ? 'text' : 'password'"
      label="Password *"
    >
      <template v-slot:append>
        <q-icon
          :name="isPwdShown ? 'visibility' : 'visibility_off'"
          class="cursor-pointer"
          @click="isPwdShown = !isPwdShown"
        />
      </template>
    </q-input>

    <div class="q-mt-md">
      <q-btn :label="(isCreate) ? createText : loginText" type="submit" color="accent" class="w-100"/>
    </div>
  </q-form>
</template>

<script>
import formUtil from 'src/utils/form'
import { useAuthStore, USER_TYPES } from 'stores/auth-store'
import { getAjaxFormData } from 'src/utils/requests'

export default {
  name: 'AuthEmailForm',
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
        this.$router.push('/dashboard')
      } else {
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
    const store = useAuthStore()
    return { store }
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
