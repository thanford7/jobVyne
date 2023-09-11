<template>
  <q-input
    filled
    :label="labelOverride || 'URL'"
    lazy-rules
    :rules="[
      val => isGoodValue(val) || 'The URL must be valid',
      val => !val || val.length <= 200 || 'URL must be less than or equal to 200 characters'
    ]"
  />
</template>

<script>
import formUtil from 'src/utils/form.js'

export default {
  name: 'InputURL',
  props: {
    isRequired: Boolean,
    labelOverride: [String, null]
  },
  data () {
    return {
      formUtil
    }
  },
  methods: {
    isGoodValue (val) {
      if (!this.isRequired && ((!val?.length) || formUtil.isGoodWebLink(val))) {
        return true
      } else if (this.isRequired && this.modelValue?.length && formUtil.isGoodWebLink(val)) {
        return true
      }
      return false
    }
  }
}
</script>
