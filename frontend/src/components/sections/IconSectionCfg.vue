<template>
  <BaseMultiPartSectionCfg
    part-label="icon"
    :section="section"
    :section-idx="sectionIdx"
  >
    <template v-slot:default="{part}">
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
    <template v-slot:liveView>
      <IconSection :section="section"/>
    </template>
  </BaseMultiPartSectionCfg>
</template>

<script>
import IconPicker from 'components/inputs/IconPicker.vue'
import IconSection from 'components/sections/IconSection.vue'
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'
import BaseMultiPartSectionCfg from 'components/sections/BaseMultiPartSectionCfg.vue'

export default {
  name: 'IconSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number
  },
  components: { BaseMultiPartSectionCfg, IconPicker, IconSection, WysiwygEditor }
}
</script>
