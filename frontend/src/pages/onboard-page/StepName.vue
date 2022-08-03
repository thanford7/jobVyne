<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <BaseStep
    title="Introduce yourself"
  >
    <div class="col-12 col-md-6 q-pa-sm">
      <q-input
        filled
        v-model="formData.first_name"
        label="First name"
        lazy-rules
        :rules="[
          val => val && val.length > 0 || 'First name is required'
        ]"
      />
    </div>
    <div class="col-12 col-md-6 q-pa-sm">
      <q-input
        filled
        v-model="formData.last_name"
        label="Last name"
        lazy-rules
        :rules="[
          val => val && val.length > 0 || 'Last name is required'
        ]"
      />
    </div>
    <template v-slot:buttons>
      <slot name="backButton"></slot>
      <slot v-if="canContinue" name="continueButton"></slot>
    </template>
  </BaseStep>
</template>

<script>
import BaseStep from 'pages/onboard-page/BaseStep.vue'

export default {
  name: 'StepName',
  components: { BaseStep },
  props: {
    formData: Object
  },
  computed: {
    canContinue () {
      return this.formData.first_name && this.formData.last_name
    }
  }
}
</script>
