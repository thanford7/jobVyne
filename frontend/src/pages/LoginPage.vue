<template>
  <div class="login-container">
    <q-page padding>
      <BannerMessage/>
      <div class="row justify-center items-center" style="height: 75vh;">
        <q-card class="col-10 col-md-4 col-lg-3">
          <q-card-section>
            <div class="flex justify-center">
              <img src="../assets/jobVyneLogoOnly.png" alt="Logo" style="height: 70px; object-fit: scale-down">
            </div>
            <h5 class="text-center">Welcome back!</h5>
          </q-card-section>
          <q-card-section>
            <q-btn
              type="div"
              class="full-width q-mt-md btn-bordered"
              :flat="true"
              :unelevated="true"
              @click="redirectAuthUrl('facebook')"
            >
              <q-icon id="facebook-logo" name="fa-brands fa-facebook-square"/>
              &nbsp;Login with Facebook
            </q-btn
            >
          </q-card-section>
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
  </div>
</template>

<script>
import { useAuthStore } from 'stores/auth-store'
import { useSocialAuthStore } from 'stores/social-auth-store'
import BannerMessage from 'components/BannerMessage.vue'
import validation from 'src/utils/validation'

export default {
  name: 'PageName',
  components: { BannerMessage },
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
    },
    async redirectAuthUrl (provider) {
      window.location = await this.socialStore.getOauthUrl(provider)
    }
  },
  created () {
    this.$api.get('auth/login-set-cookie/')
  },
  setup () {
    const store = useAuthStore()
    const socialStore = useSocialAuthStore()
    return { store, socialStore }
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
    background: url('../assets/background/connectwork.png') no-repeat center center fixed;
    background-size: cover;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    opacity: 0.2;
    overflow: hidden;
  }

#facebook-logo {
  color: $facebook
}
}
</style>
