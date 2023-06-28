<template>
  <q-input
    filled
    :label="labelOverride || 'LinkedIn URL'"
    hint="www.linkedin.com/in/{profile id}"
    lazy-rules
    :rules="[
      val => {
        if (!isRequired && (!val?.length || formUtil.isGoodLinkedInUrl(val))) {
          return true
        } else if (isRequired && val?.length && formUtil.isGoodLinkedInUrl(val)) {
          return true
        }
        return 'The LinkedIn URL must be valid'
      },
      val => !val || val.length <= 200 || 'LinkedIn URL must be less than or equal to 200 characters'
    ]"
  />
</template>

<script>
import formUtil from 'src/utils/form.js'

export default {
  name: 'InputLinkedIn',
  props: {
    isRequired: Boolean,
    labelOverride: [String, null]
  },
  data () {
    return {
      formUtil
    }
  }
}
</script>
