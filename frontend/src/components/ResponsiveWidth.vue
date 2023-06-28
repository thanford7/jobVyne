<template>
  <div :class="sizeClasses">
    <slot/>
  </div>
</template>

<script>
export default {
  name: 'ResponsiveWidth',
  props: {
    isSmall: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    sizeClasses () {
      if (this.isSmall) {
        return ['col-12', 'col-md-8', 'col-lg-6']
      }
      return ['col-12', 'col-md-11', 'col-lg-9']
    }
  }
}
</script>
