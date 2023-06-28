<template>
  <q-select
    filled emit-value map-options
    :use-chips="isMulti" :multiple="isMulti"
    :options="[{val: true, label: 'Yes'}, {val: false, label: 'No'}]"
    option-value="val"
    option-label="label"
    :label="label"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
export default {
  name: 'SelectYesNo',
  props: {
    label: String,
    isMulti: {
      type: Boolean,
      default: true
    }
  }
}
</script>
