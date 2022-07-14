<template>
  <div style="display: inline-block;">
    <span v-if="is_include_space">&nbsp;</span><slot name="icon"/>
    <q-tooltip :class="color_class" style="font-size: 14px;" max-width="500px">
      <slot/>
    </q-tooltip>
  </div>
</template>

<script>
export default {
  name: 'CustomTooltip',
  props: {
    color_class: {
      type: String,
      default: 'bg-info'
    },
    is_include_space: {
      type: Boolean,
      default: true
    }
  }
}
</script>
