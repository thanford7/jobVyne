<template>
  <q-input
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    filled
    :label="label"
    lazy-rules
    :rules="[ val => val && val.length > 0 && formUtil.isGoodEmail(val) || 'Please enter a valid email']"
  />
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
    }
  },
  data () {
    return {
      formUtil
    }
  }
}
</script>
