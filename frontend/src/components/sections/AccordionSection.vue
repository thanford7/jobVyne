<template>
  <div>
    <q-expansion-item
      v-for="part in section.item_parts"
      expand-separator
      :label="part.header"
      :header-class="['text-h6']"
      :header-style="accordionStyle"
      class="border-bottom-1-gray-100 inherit-text-color"
    >
      <div class="q-pa-md bg-white" v-html="part.html_content" :style="bodyStyle"/>
    </q-expansion-item>
  </div>
</template>

<script>
import sectionUtil from 'components/sections/sectionTypes.js'
import colorUtil from 'src/utils/color.js'

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
  },
  computed: {
    accordionStyle () {
      const style = {}
      const styleOptions = [
        // cfgKey, styleKey, defaultVal
        ['accordion_header_color', 'color', colorUtil.getPaletteColor('white')],
        ['accordion_background_color', 'backgroundColor', colorUtil.getPaletteColor('primary')]
      ]
      styleOptions.forEach(([cfgKey, styleKey, defaultVal]) => {
        const val = this.section.config[cfgKey]
        style[styleKey] = val || defaultVal
      })
      return style
    },
    bodyStyle () {
      return sectionUtil.getTextStyle(this.section)
    }
  }
}
</script>
