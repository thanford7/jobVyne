<template>
  <BaseMultiPartSectionCfg
    part-label="icon"
    :section="section"
    :section-idx="sectionIdx"
  >
    <template v-slot:liveView>
      <IconSection :section="section"/>
    </template>
  </BaseMultiPartSectionCfg>
</template>

<script>
import IconSection from 'components/sections/IconSection.vue'
import BaseMultiPartSectionCfg from 'components/sections/BaseMultiPartSectionCfg.vue'

export default {
  name: 'IconSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number
  },
  components: { BaseMultiPartSectionCfg, IconSection }
}
</script>
