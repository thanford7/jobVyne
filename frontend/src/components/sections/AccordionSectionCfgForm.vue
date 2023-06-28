<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12">
    <q-input filled v-model="part.header" label="Accordion item header"/>
  </div>
  <div class="col-12 q-mb-md">
    <WysiwygEditor2
      v-model="part.html_content"
      placeholder="Accordion text..."
    />
  </div>
</template>

<script>
import WysiwygEditor2 from 'components/inputs/WysiwygEditor2.vue'

export default {
  name: 'AccordionSectionCfgForm',
  components: { WysiwygEditor2 },
  props: {
    part: Object
  }
}
</script>

<style scoped>

</style>
