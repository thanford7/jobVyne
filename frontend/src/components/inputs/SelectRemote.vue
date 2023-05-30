<template>
  <q-select
    ref="select"
    filled clearable emit-value map-options
    :options="[{val: locationUtil.REMOTE_TYPE_TRUE, label: 'Yes'}, {val: locationUtil.REMOTE_TYPE_FALSE, label: 'No'}]"
    option-value="val"
    option-label="label"
    label="Remote"
  />
</template>

<script>
import locationUtil from 'src/utils/location.js'

export default {
  name: 'SelectRemote',
  data () {
    return {
      locationUtil
    }
  }
}
</script>
