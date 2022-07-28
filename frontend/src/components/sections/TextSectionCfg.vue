<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <div class="col-12">
    <WysiwygEditor
      v-model="section.item_parts[0].html_content"
      placeholder="Section text..."
    />
  </div>
  <LiveView :section="section">
      <SectionHeader :section="section"/>
      <TextSection :section="section"/>
  </LiveView>
</template>

<script>
import LiveView from 'components/sections/LiveView.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import TextSection from 'components/sections/TextSection.vue'
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'

export default {
  name: 'TextSectionCfg',
  props: {
    section: Object
  },
  components: { TextSection, LiveView, SectionHeader, WysiwygEditor }
}
</script>
