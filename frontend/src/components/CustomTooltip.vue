<template>
  <div style="display: inline-block;">
    <slot name="content"/>
    <span v-if="is_include_space">&nbsp;</span>
    <slot name="icon">
      <q-icon v-if="is_include_icon" :class="icon_color_class" tag="span" name="help_outline" :size="icon_size"/>
    </slot>
    <Tooltip>
      <slot/>
    </Tooltip>
  </div>
</template>

<script>
import Tooltip from 'components/Tooltip.vue'
export default {
  name: 'CustomTooltip',
  components: { Tooltip },
  props: {
    icon_color_class: {
      type: String,
      default: 'text-gray-500'
    },
    icon_size: {
      type: String,
      default: '24px'
    },
    is_include_space: {
      type: Boolean,
      default: false
    },
    is_include_icon: {
      type: Boolean,
      default: true
    }
  }
}
</script>
