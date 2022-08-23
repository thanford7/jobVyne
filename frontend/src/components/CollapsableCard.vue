<template>
  <q-card>
    <div class="row q-py-sm q-pr-md border-bottom-1-gray-100 bg-grey-2">
      <div class="text-h6 q-ml-md">{{ title }}</div>
      <q-space/>
      <slot name="header"/>
      <q-btn
        color="grey-7"
        flat dense
        :icon="isUserFilterExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="isUserFilterExpanded = !isUserFilterExpanded"
      />
    </div>
    <q-slide-transition>
      <div v-show="isUserFilterExpanded" class="row">
        <slot name="body"/>
      </div>
    </q-slide-transition>
  </q-card>
</template>

<script>
export default {
  name: 'CollapsableCard',
  props: {
    title: String
  },
  data () {
    return {
      isUserFilterExpanded: true
    }
  }
}
</script>

<style scoped>

</style>
