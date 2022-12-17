<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12 col-md-6 q-pr-md-sm">
    <q-input filled v-model="part.header" label="Icon header"/>
  </div>
  <div class="col-12 col-md-6 q-pl-md-sm">
    <IconPicker v-model="part.icon"/>
  </div>
  <div class="col-12 q-mb-md">
    <WysiwygEditor
      placeholder="Text below the icon..."
      v-model="part.html_content"/>
  </div>
</template>

<script>
import IconPicker from 'components/inputs/IconPicker.vue'
import WysiwygEditor from 'components/inputs/WysiwygEditor.vue'

export default {
  name: 'IconSectionCfgForm',
  components: { IconPicker, WysiwygEditor },
  props: {
    part: Object
  }
}
</script>
