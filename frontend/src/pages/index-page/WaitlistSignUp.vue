<template>
  <div class="q-px-lg">
    <q-input
      ref="emailInput"
      filled
      v-model="email"
      label="Email"
      lazy-rules="ondemand"
      :loading="isSavingWaitlist"
      :rules="[ val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'Please enter a valid email']"
      v-on:keyup.enter="saveWaitlist"
    >
      <template v-slot:after>
        <q-btn class="h-100" color="accent" ripple unelevated @click="saveWaitlist">
          Join waitlist
        </q-btn>
      </template>
    </q-input>
    <div class="text-small text-grey-7">
      This site is protected by reCAPTCHA and the Google
      <a href="https://policies.google.com/privacy">Privacy Policy</a> and
      <a href="https://policies.google.com/terms">Terms of Service</a> apply.
    </div>
  </div>
</template>

<script>
import { getAjaxFormData } from 'src/utils/requests'
import formUtil from 'src/utils/form'
import { useAuthStore } from 'stores/auth-store'
import { msgClassCfgs, useAjaxStore } from 'stores/ajax-store'

export default {
  name: 'WaitlistSignUp',
  data () {
    return {
      email: null,
      isSavingWaitlist: false,
      formUtil
    }
  },
  methods: {
    async saveWaitlist () {
      if (!this.$refs.emailInput.validate()) {
        return
      }
      this.isSavingWaitlist = true
      this.authStore.executeIfCaptchaValid(
        'WAITLIST',
        async () => {
          await this.$api.post('waitlist/', getAjaxFormData({ email: this.email }))
        },
        () => this.ajaxStore.addMsg('Unable to complete waitlist sign up. reCAPTCHA authentication failed', msgClassCfgs.ERROR),
        () => {
          this.isSavingWaitlist = false
          this.email = null
          this.$refs.emailInput.blur()
        }
      )
    }
  },
  setup () {
    return { ajaxStore: useAjaxStore(), authStore: useAuthStore() }
  }
}
</script>

<style scoped>

</style>
