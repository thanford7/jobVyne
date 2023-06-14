<template>
  <q-card>
    <div
      class="row q-px-md border-bottom-1-gray-100 bg-grey-2 items-center"
      :class="(isDense) ? '' : 'q-py-sm'"
    >
      <div class="text-h6 text-h6--mobile q-ml-md">{{ title }}</div>
      <slot name="header-left"/>
      <q-space/>
      <slot name="header"/>
      <q-btn
        v-if="canCollapse"
        color="grey-7"
        flat dense
        :icon="isExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="isExpanded = !isExpanded"
      />
    </div>
    <q-slide-transition>
      <div v-show="isExpanded" class="row q-px-sm q-gutter-y-sm">
        <slot name="body"/>
      </div>
    </q-slide-transition>
  </q-card>
</template>

<script>
export default {
  name: 'CollapsableCard',
  props: {
    title: [String, null],
    isDense: {
      type: Boolean,
      default: false
    },
    canCollapse: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      isExpanded: true
    }
  }
}
</script>

<style scoped>

</style>
