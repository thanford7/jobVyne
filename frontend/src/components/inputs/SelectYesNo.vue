<template>
  <q-select
    filled multiple emit-value map-options use-chips
    :options="[{val: true, label: 'Yes'}, {val: false, label: 'No'}]"
    option-value="val"
    option-label="label"
    :label="label"
  />
</template>

<script>
export default {
  name: 'SelectYesNo',
  props: {
    label: String
  }
}
</script>
