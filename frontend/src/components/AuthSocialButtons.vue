<template>
  <div class="q-gutter-y-sm">
    <div v-for="platform in authPlatforms" class="flex flex-center">
      <AuthSocialButton
        :platform="platform"
        :button-text="`${(isCreate) ? createText : loginText}${platform.name}`"
        @click="redirectAuthUrl(platform.redirectProvider)"
      />
    </div>
  </div>
</template>

<script>
import AuthSocialButton from 'components/AuthSocialButton.vue'
import socialUtil from 'src/utils/social.js'
import { useSocialAuthStore } from 'stores/social-auth-store'

export default {
  name: 'AuthSocialButtons',
  components: { AuthSocialButton },
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
