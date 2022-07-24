<template>
  <div>
    <q-expansion-item
      v-for="(part, partIdx) in section.section_parts"
      :group="`section-${sectionIdx}-parts`"
      default-opened dense expand-separator
      :header-class="['bg-grey-3']"
    >
      <template v-slot:header>
        <span class="q-pt-xs" style="font-size: 1.2em">
          {{ part.header || `Icon # ${partIdx + 1}` }}
        </span>
        <q-space/>
        <div class="q-px-sm q-mx-md border-left-1-white border-right-1-white">
          <q-btn
            v-if="partIdx !== 0"
            flat dense icon="arrow_upward"
            @click="$emit('moveUp', partIdx)"/>
          <q-btn
            v-if="partIdx !== section.section_parts.length - 1"
            flat dense icon="arrow_downward"
            @click="$emit('moveDown', partIdx)"/>
          <q-btn
            flat dense icon="delete" text-color="negative"
            @click="$emit('remove', partIdx)"/>
        </div>
      </template>
      <div class="row q-gutter-y-sm q-mt-sm q-px-sm">
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
      </div>
    </q-expansion-item>
    <div class="q-mt-md">
      <q-btn
        no-caps icon="add"
        color="primary"
        @click="$emit('add')"
      >
        Add icon item
      </q-btn>
    </div>
    <LiveView>
      <IconSection :section="section"/>
    </LiveView>
  </div>
</template>

<script>
import IconPicker from 'components/inputs/IconPicker.vue'
import IconSection from 'components/sections/IconSection.vue'
import WysiwygEditor from 'components/section-editors/WysiwygEditor.vue'
import LiveView from 'components/sections/LiveView.vue'

export default {
  name: 'IconSectionCfg',
  props: {
    section: Object,
    sectionIdx: Number
  },
  components: { LiveView, IconPicker, IconSection, WysiwygEditor }
}
</script>
