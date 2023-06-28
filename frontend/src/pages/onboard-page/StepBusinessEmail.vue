<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Add a business email"
  >
    <q-form ref="form" @submit.prevent>
      <div class="row">
        <div class="col-12 col-md-6">
          <EmailInput
            v-model="formData.business_email"
            label="Business email" autofocus
            :is-required="false"
            :additional-rules="[
              val => val !== personalEmail || 'Business email must be different than personal email'
            ]"
            @keyup.enter.prevent="$emit('continue')"
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
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    }
  }
}
</script>
