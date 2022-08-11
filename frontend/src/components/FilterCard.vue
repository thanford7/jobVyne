<template>
  <q-card>
    <div class="row q-ml-sm q-py-sm q-pr-md">
      <div class="text-h6 q-ml-sm">{{ title }}</div>
      <q-space/>
      <q-btn
        color="grey-7"
        flat dense
        :icon="isUserFilterExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        @click="isUserFilterExpanded = !isUserFilterExpanded"
      />
    </div>
    <q-slide-transition>
      <div v-show="isUserFilterExpanded" class="row">
        <slot name="filters"/>
      </div>
    </q-slide-transition>
  </q-card>
</template>

<script>
export default {
  name: 'FilterCard',
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
