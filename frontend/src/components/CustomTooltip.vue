<template>
  <div style="display: inline-block;">
    <span v-if="is_include_space">&nbsp;</span>
    <slot name="icon">
      <q-icon v-if="is_include_icon" class="text-gray-500" tag="span" name="help_outline" :size="icon_size"/>
    </slot>
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
    icon_size: {
      type: String,
      default: '24px'
    },
    is_include_space: {
      type: Boolean,
      default: true
    },
    is_include_icon: {
      type: Boolean,
      default: true
    }
  }
}
</script>
