<template>
  <q-card>
    <div
      class="row q-pr-md border-bottom-1-gray-100 bg-grey-2 items-center"
      :class="(isDense) ? '' : 'q-py-sm'"
    >
      <div class="text-h6 q-ml-md">{{ title }}</div>
      <slot name="header-left"/>
      <q-space/>
      <slot name="header"/>
      <q-btn
        color="grey-7"
        flat dense
        :icon="isExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="isExpanded = !isExpanded"
      />
    </div>
    <q-slide-transition>
      <div v-show="isExpanded" class="row">
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
