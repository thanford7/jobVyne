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
  </div>
</template>

<script>
import { getAjaxFormData } from 'src/utils/requests'
import formUtil from 'src/utils/form'

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
      await this.$api.post('waitlist/', getAjaxFormData({ email: this.email }))
      this.isSavingWaitlist = false
      this.email = null
      this.$refs.emailInput.blur()
    }
  }
}
</script>

<style scoped>

</style>
