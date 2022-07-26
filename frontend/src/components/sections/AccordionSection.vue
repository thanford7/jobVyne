<template>
  <div>
    <q-expansion-item
      v-for="part in section.section_parts"
      default-opened dense expand-separator
      :label="part.header"
      :header-class="['bg-primary', 'text-white']"
    >
      <div class="q-pa-md" v-html="part.html_content"/>
    </q-expansion-item>
  </div>
</template>

<script>
let idx = 0
export default {
  name: 'AccordionSection',
  props: {
    section: {
      type: [Object, null]
    },
    isAccordionMode: {
      type: Boolean,
      default: false
    }
  },
  data () {
    idx++
    return {
      accordionIdx: idx
    }
  }
}
</script>
