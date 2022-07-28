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
export default {
  name: 'LiveView',
  props: {
    section: Object
  },
  computed: {
    sectionStyle () {
      const backgroundColor = this.section.config.background_color
      if (backgroundColor) {
        return { backgroundColor }
      }
      return {}
    }
  }
}
</script>
