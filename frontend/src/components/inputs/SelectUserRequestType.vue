<template>
  <q-select
    autofocus filled map-options emit-value
    :options="options"
    option-value="key"
    option-label="label"
    label="Request type"
    :rules="[
      (val) => dataUtil.getBoolean(val) || 'Request type is required'
    ]"
  />
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { USER_REQUEST_TYPES } from 'src/utils/karma.js'

export default {
  name: 'SelectUserRequestType',
  data () {
    return {
      dataUtil
    }
  },
  computed: {
    options () {
      return Object.values(USER_REQUEST_TYPES).map((urt) => dataUtil.pick(urt, ['key', 'label']))
    }
  }
}
</script>
