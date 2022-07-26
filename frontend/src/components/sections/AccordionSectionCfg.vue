<template>
  <BaseMultiPartSectionCfg
    part-label="accordion"
    :section="section"
    :section-idx="sectionIdx"
  >
    <template v-slot:default="{part}">
      <div class="col-12">
        <q-input filled v-model="part.header" label="Accordion item header"/>
      </div>
      <div class="col-12">
        <WysiwygEditor
          v-model="part.html_content"
          placeholder="Accordion text..."
        />
      </div>
    </template>
    <template v-slot:liveView>
      <AccordionSection :section="section"/>
    </template>
  </BaseMultiPartSectionCfg>
</template>

<script>
import AccordionSection from 'components/sections/AccordionSection.vue'
import BaseMultiPartSectionCfg from 'components/sections/BaseMultiPartSectionCfg.vue'
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'

export default {
  name: 'AccordionSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number
  },
  components: { BaseMultiPartSectionCfg, AccordionSection, WysiwygEditor }
}
</script>
