<template>
<!--  eslint-disable vue/no-mutating-props-->
  {{ col.label }}
  <TableFilter filter-name="Job title" :has-filter="hasFilter">
    <q-input
      v-model="jobsFilter.jobTitle"
      filled borderless autofocus debounce="300"
      placeholder="Job title"
    >
      <template v-slot:append>
        <q-icon name="search"/>
      </template>
    </q-input>
  </TableFilter>
</template>

<script>
import TableFilter from 'components/tables/TableFilter.vue'

export default {
  name: 'JobTitleHeader',
  props: {
    col: Object,
    jobsFilter: Object
  },
  computed: {
    hasFilter () {
      return Boolean(this.jobsFilter.jobTitle) && Boolean(this.jobsFilter.jobTitle.length)
    }
  },
  components: { TableFilter }
}
</script>
