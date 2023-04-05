<template>
  <div class="q-gutter-y-sm">
    <q-btn
      v-for="platform in authPlatforms"
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
import socialUtil from 'src/utils/social.js'
import { useSocialAuthStore } from 'stores/social-auth-store'

export default {
  name: 'AuthSocialButtons',
  data () {
    return {
      createText: 'Create with ',
      loginText: 'Login with ',
      authPlatforms: [
        socialUtil.platformCfgs[socialUtil.SOCIAL_KEY_LINKED_IN],
        socialUtil.platformCfgs[socialUtil.SOCIAL_KEY_GOOGLE]
      ]
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
