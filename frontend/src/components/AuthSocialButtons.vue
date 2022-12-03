<template>
  <div class="q-gutter-y-sm">
    <q-btn
      v-for="platform in AUTH_PLATFORMS"
      type="div"
      class="w-100 btn-bordered"
      ripple flat unelevated
      @click="redirectAuthUrl(platform.redirectProvider)"
    >
      <q-icon tag="div" :name="`fa-brands ${platform.icon}`" class="q-mr-sm"/>
      <div class="text-center">
        {{ (isCreate) ? createText : loginText }}{{ platform.name }}
      </div>
    </q-btn>
  </div>
</template>

<script>
import { useSocialAuthStore } from 'stores/social-auth-store'

const AUTH_PLATFORMS = [
  {
    name: 'LinkedIn',
    icon: 'fa-linkedin-in',
    redirectProvider: 'linkedin-oauth2'
  },
  {
    name: 'Google',
    icon: 'fa-google',
    redirectProvider: 'google-oauth2'
  }
  // {
  //   name: 'Facebook',
  //   icon: 'fa-facebook-f',
  //   redirectProvider: 'facebook'
  // }
]

export default {
  name: 'AuthSocialButtons',
  data () {
    return {
      createText: 'Create with ',
      loginText: 'Login with ',
      AUTH_PLATFORMS
    }
  },
  props: {
    isCreate: { // Whether the user is creating an account or logging in
      type: Boolean,
      default: false
    },
    userTypeBit: {
      type: [Number, null]
    },
    redirectPageUrl: {
      type: [String, null]
    },
    redirectParams: {
      type: [Object, null]
    }
  },
  methods: {
    async redirectAuthUrl (provider) {
      const url = await this.socialAuthStore.getOauthUrl(
        provider,
        { redirectPageUrl: this.redirectPageUrl, redirectParams: this.redirectParams, userTypeBit: this.userTypeBit }
      )
      window.location.href = url
    }
  },
  created () {
    this.$api.get('auth/login-set-cookie/')
  },
  setup () {
    const socialAuthStore = useSocialAuthStore()
    return { socialAuthStore }
  }
}
</script>
