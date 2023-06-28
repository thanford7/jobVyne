<template>
  <div>
    <h4
      v-if="section.header"
      class="q-mb-lg"
      :id="(isIncludeElId) ? `employer-${sectionIdx}` : null"
      :style="headerStyle"
    >
      {{ section.header }}
    </h4>
  </div>
</template>

<script>
export default {
  name: 'SectionHeader',
  props: {
    section: Object,
    sectionIdx: [Number, null],
    isIncludeElId: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    headerStyle () {
      const headerColor = this.section.config.header_color
      if (headerColor) {
        return { color: headerColor }
      }
      return {}
    }
  }
}
</script>
