<template>
  <div style="display: inline-block">
    <q-icon
      :title="`Filter ${filterName}`"
      class="table-filter" :class="(hasFilter) ? 'table-filter-active' : ''"
      name="filter_alt" color="grey-8" size="16px" @click="openDialog"
    />
    <DialogBase v-model="isOpen" :base-title-text="`${filterName} filter`" :is-include-buttons="false">
      <template v-slot:default>
        <slot/>
      </template>
    </DialogBase>
  </div>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'

export default {
  name: 'TableFilter',
  components: { DialogBase },
  props: {
    filterName: String,
    hasFilter: {
      type: [Boolean, Number],
      default: false
    }
  },
  data () {
    return {
      isOpen: false
    }
  },
  methods: {
    openDialog (e) {
      e.preventDefault()
      e.stopPropagation()
      this.isOpen = true
    }
  }
}
</script>

<style lang="scss" scoped>
.table-filter {
  display: none;
  &.table-filter-active {
    display: inline;
  }
}
th:hover .table-filter {
  display: inline;
}
</style>
