<template>
  <div>
    <div v-html="section.item_parts[0].html_content" :style="bodyStyle"/>
  </div>
</template>

<script>
import sectionUtil from 'components/sections/sectionTypes.js'

export default {
  name: 'TextSection',
  props: {
    section: Object
  },
  computed: {
    bodyStyle () {
      return sectionUtil.getTextStyle(this.section)
    }
  }
}
</script>
