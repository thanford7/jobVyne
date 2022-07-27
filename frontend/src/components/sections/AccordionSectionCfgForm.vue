<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12">
    <q-input filled v-model="part.header" label="Accordion item header"/>
  </div>
  <div class="col-12 q-mb-md">
    <WysiwygEditor
      v-model="part.html_content"
      placeholder="Accordion text..."
    />
  </div>
</template>

<script>
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'

export default {
  name: 'AccordionSectionCfgForm',
  components: { WysiwygEditor },
  props: {
    part: Object
  }
}
</script>

<style scoped>

</style>
