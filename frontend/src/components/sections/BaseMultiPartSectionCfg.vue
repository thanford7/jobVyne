<template>
  <div>
    <q-expansion-item
      v-for="(part, partIdx) in section.item_parts"
      :group="`section-${sectionIdx}-parts`"
      default-opened dense expand-separator
      :header-class="['bg-grey-3']"
      class="border-bottom-1-gray-300"
    >
      <template v-slot:header>
        <span class="q-pt-xs" style="font-size: 1.2em">
          {{ part.header || `${dataUtil.capitalize(partLabel)} #${partIdx + 1}` }}
        </span>
        <q-space/>
        <div class="q-px-sm q-mx-md border-left-1-white border-right-1-white">
          <q-btn
            v-if="partIdx !== 0"
            flat dense icon="arrow_upward"
            @click="$emit('moveUp', partIdx)"/>
          <q-btn
            v-if="partIdx !== section.item_parts.length - 1"
            flat dense icon="arrow_downward"
            @click="$emit('moveDown', partIdx)"/>
          <q-btn
            flat dense icon="delete" text-color="negative"
            @click="$emit('remove', partIdx)"/>
        </div>
      </template>
      <div class="row q-gutter-y-sm q-mt-sm q-px-sm">
        <IconSectionCfgForm v-if="section.type === SECTION_TYPES.ICON.key" :part="part"/>
        <AccordionSectionCfgForm v-if="section.type === SECTION_TYPES.ACCORDION.key" :part="part"/>
      </div>
    </q-expansion-item>
    <div class="q-mt-md">
      <q-btn
        no-caps icon="add"
        color="primary"
        @click="$emit('add')"
      >
        Add {{ partLabel }} item
      </q-btn>
    </div>
    <LiveView :section="section">
      <SectionHeader :section="section"/>
      <slot name="liveView"/>
    </LiveView>
  </div>
</template>

<script>
import AccordionSectionCfgForm from 'components/sections/AccordionSectionCfgForm.vue'
import IconSectionCfgForm from 'components/sections/IconSectionCfgForm.vue'
import LiveView from 'components/sections/LiveView.vue'
import SectionHeader from 'components/sections/SectionHeader.vue'
import { SECTION_TYPES } from 'components/sections/sectionTypes.js'
import dataUtil from 'src/utils/data'

export default {
  name: 'BaseMultiPartSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number,
    partLabel: String
  },
  components: { SectionHeader, AccordionSectionCfgForm, IconSectionCfgForm, LiveView },
  data () {
    return {
      dataUtil,
      SECTION_TYPES
    }
  }
}
</script>
