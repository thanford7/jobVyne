<template>
  <q-list>
    <q-item v-for="(item, idx) in items" :key="idx">
      <q-item-section avatar>
        <q-icon :color="getColor(item)" :name="getIcon(item)"/>
      </q-item-section>
      <q-item-section>
        {{ getText(item) }}
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script>
import dataUtil from 'src/utils/data'

export default {
  name: 'ListIcon',
  props: {
    // ['<item text>', {text: '<item text>', color: '<item color>', icon: '<item icon>'}]
    // In object form:
    //    text is required
    //    color and icon are optional. If not supplied, defaults are used
    items: { type: Array },
    color: { type: String },
    iconName: { type: String }
  },
  methods: {
    getText (item) {
      return (dataUtil.isObject(item)) ? item.text : item
    },
    getColor (item) {
      if (dataUtil.isObject(item)) {
        return item.color || this.color
      }
      return this.color
    },
    getIcon (item) {
      if (dataUtil.isObject(item)) {
        return item.icon || this.iconName
      }
      return this.iconName
    }
  }
}
</script>

<style scoped>

</style>
