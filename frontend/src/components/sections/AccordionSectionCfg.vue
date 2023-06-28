<template>
  <BaseMultiPartSectionCfg
    part-label="accordion"
    :section="section"
    :section-idx="sectionIdx"
  >
    <template v-slot:liveView>
      <AccordionSection :section="section"/>
    </template>
  </BaseMultiPartSectionCfg>
</template>

<script>
import AccordionSection from 'components/sections/AccordionSection.vue'
import BaseMultiPartSectionCfg from 'components/sections/BaseMultiPartSectionCfg.vue'

export default {
  name: 'AccordionSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number
  },
  components: { BaseMultiPartSectionCfg, AccordionSection }
}
</script>
