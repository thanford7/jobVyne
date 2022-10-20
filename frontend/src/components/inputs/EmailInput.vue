<template>
  <q-input
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    filled :label="label" lazy-rules
    class="jv-email"
    :rules="rules"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-input>
</template>

<script>
import formUtil from 'src/utils/form.js'

export default {
  name: 'EmailInput',
  props: {
    modelValue: [String, null],
    label: {
      type: String,
      default: 'Email'
    },
    isRequired: {
      type: Boolean,
      default: true
    },
    additionalRules: {
      type: Array,
      default: () => ([])
    }
  },
  computed: {
    rules () {
      const rules = [
        (val) => {
          if (this.isRequired && (!val || !val.length)) {
            return 'An email is required'
          }
          if (val && val.length > 0 && !formUtil.isGoodEmail(val)) {
            return 'Please enter a valid email'
          }
          return true
        },
        ...this.additionalRules
      ]

      return rules
    }
  },
  data () {
    return {
      formUtil
    }
  }
}
</script>
