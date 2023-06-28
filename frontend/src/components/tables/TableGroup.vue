<template>
  <q-icon
    :title="`Group by ${groupName}`"
    class="table-group" :class="(isGrouped) ? 'table-group-active' : ''"
    name="join_full" color="grey-8" size="16px" @click="handleGroup"
  />
</template>

<script>
export default {
  name: 'TableGroup',
  props: {
    groupName: String
  },
  data () {
    return {
      isGrouped: false
    }
  },
  methods: {
    handleGroup (e) {
      e.preventDefault()
      e.stopPropagation()
      this.isGrouped = !this.isGrouped
      this.$emit('group-toggle', this.isGrouped)
    }
  }
}
</script>

<style lang="scss" scoped>
.table-group {
  display: none;
  &.table-group-active {
    display: inline;
  }
}
th:hover .table-group {
  display: inline;
}
</style>
