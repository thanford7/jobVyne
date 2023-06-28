<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Select your current employer"
  >
    <q-form ref="form">
      <div class="row">
        <div class="col-12 col-md-6">
          <q-select
            id="jv-employer-sel"
            filled emit-value map-options autofocus
            v-model="formData.employer_id"
            :options="potentialEmployers"
            autocomplete="name"
            option-value="id"
            option-label="name"
            label="Employer"
            lazy-rules
            :rules="[val => val || 'Please select an option']"
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

export default {
  name: 'StepSelectEmployer',
  components: { BaseStep },
  props: {
    formData: Object,
    potentialEmployers: Array
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
