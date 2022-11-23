<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Add your employer's name"
    sub-title="It doesn't look like your employer has an account with JobVyne. You can still complete your profile and we will notify you if your employer creates an account."
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12 col-md-6">
          <q-input
            class="jv-employer-unknown"
            filled
            v-model="formData.unknown_employer_name"
            label="Employer name"
            lazy-rules
            :rules="[
          val => val && val.length > 0 || 'A name is required',
          val => val.length <= 100 || 'The maximum character length is 100'
        ]"
          />
        </div>
      </div>
    </q-form>
    <template v-slot:buttons>
      <slot name="backButton"></slot>
      <slot v-if="canContinue" name="continueButton"></slot>
    </template>
  </BaseStep>
</template>

<script>
import BaseStep from 'pages/onboard-page/BaseStep.vue'

export default {
  name: 'StepUnknownEmployer',
  components: { BaseStep },
  props: {
    formData: Object
  },
  computed: {
    canContinue () {
      return Boolean(this.formData.unknown_employer_name)
    }
  },
  methods: {
    async isValidForm () {
      return await this.$refs.form.validate()
    }
  }
}
</script>
