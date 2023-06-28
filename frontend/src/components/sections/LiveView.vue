<template>
  <div class="q-mt-md">
    <q-expansion-item
      default-opened dense
      :header-class="['bg-grey-3']"
    >
      <template v-slot:header>
        <q-item-section>
          Live view
        </q-item-section>
      </template>
      <div class="q-pa-sm" :style="sectionStyle">
        <slot/>
      </div>
    </q-expansion-item>
  </div>
</template>

<script>
import sectionUtil from 'components/sections/sectionTypes.js'

export default {
  name: 'LiveView',
  props: {
    section: Object
  },
  computed: {
    sectionStyle () {
      return sectionUtil.getBackgroundStyle(this.section)
    }
  }
}
</script>
