<template>
  <q-page padding>
    <div class="row justify-center items-center" style="height: 75vh;">
      <q-card class="col-10 col-lg-8">
        <q-card-section>
          <q-form
            @submit="login"
            class="q-gutter-md"
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

            <div>
              <q-btn label="Login" type="submit" color="primary"/>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { useAuthStore } from 'stores/auth-store'
import validation from 'src/utils/validation'

export default {
  name: 'PageName',
  data () {
    return {
      email: null,
      password: null,
      isPwdShown: false
    }
  },
  methods: {
    isGoodEmail: validation.isGoodEmail,
    async login () {
      const user = {
        email: this.email,
        password: this.password
      }
      const login = this.store.login.bind(this.store)
      await login(user)
      this.$router.push('/')
      this.email = null
      this.password = null
    }
  },
  created () {
    this.$api.get('auth/login-set-cookie/')
  },
  setup () {
    const store = useAuthStore()
    return { store }
  }
}
</script>
