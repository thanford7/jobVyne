<template>
  <div>
    <q-expansion-item
      v-for="part in section.item_parts"
      expand-separator
      :label="part.header"
      :header-class="['bg-primary', 'text-white', 'text-h6']"
      expand-icon-class="text-white"
      class="border-bottom-1-gray-100"
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
