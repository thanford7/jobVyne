<template>
  <div>
    <q-btn
      type="div"
      class="w-100 btn-bordered"
      :flat="true"
      :unelevated="true"
      @click="redirectAuthUrl('facebook')"
    >
      <q-icon id="facebook-logo" name="fa-brands fa-facebook-square"/>
      &nbsp;{{ (isCreate) ? createText : loginText }}Facebook
    </q-btn
    >
  </div>
</template>

<script>
import { useSocialAuthStore } from 'stores/social-auth-store'
import { USER_TYPES } from 'stores/auth-store'

export default {
  name: 'AuthSocialButtons',
  data () {
    return {
      createText: 'Create account with ',
      loginText: 'Login with '
    }
  },
  props: {
    isCreate: { // Whether the user is creating an account or logging in
      type: Boolean,
      default: false
    },
    userTypeBit: {
      type: Number,
      default: USER_TYPES.USER_TYPE_EMPLOYEE
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
      const url = await this.socialStore.getOauthUrl(
        provider,
        { redirectPageUrl: this.redirectPageUrl, redirectParams: this.redirectParams }
      )
      window.location.href = url
    }
  },
  created () {
    this.$api.get('auth/login-set-cookie/')
  },
  setup () {
    const socialStore = useSocialAuthStore()
    return { socialStore }
  }
}
</script>

<style lang="scss" scoped>
#facebook-logo {
  color: $facebook
}
</style>
