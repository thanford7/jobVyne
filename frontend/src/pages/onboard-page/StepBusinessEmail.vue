<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Add a business email"
  >
    <div class="col-12 col-md-6">
      <EmailInput v-model="email" label="Business email" @blur="formData.business_email = email"/>
    </div>
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
    formData: Object,
    potentialEmployers: [Array, null]
  },
  data () {
    return {
      email: null
    }
  },
  mounted () {
    if (!this.email && this.formData.business_email) {
      this.email = this.formData.business_email
    }
  }
}
</script>
