<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Add a business email"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12 col-md-6">
          <EmailInput
            v-model="email"
            label="Business email"
            :is-required="false"
            :additional-rules="[
              val => val !== personalEmail || 'Business email must be different than personal email'
            ]"
            @blur="formData.business_email = email"
          />
        </div>
      </div>
    </q-form>
    <template v-slot:buttons>
      <slot name="backButton"></slot>
      <slot name="continueButton"></slot>
    </template>
  </BaseStep>
</template>

<script>
import BaseStep from 'pages/onboard-page/BaseStep.vue'
import EmailInput from 'components/inputs/EmailInput.vue'

export default {
  name: 'StepBusinessEmail',
  components: { BaseStep, EmailInput },
  props: {
    personalEmail: String,
    formData: Object
  },
  data () {
    return {
      email: null
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    }
  },
  mounted () {
    if (!this.email && this.formData.business_email) {
      this.email = this.formData.business_email
    }
  }
}
</script>
