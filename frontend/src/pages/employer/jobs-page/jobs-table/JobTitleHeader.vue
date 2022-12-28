<template>
<!--  eslint-disable vue/no-mutating-props-->
  {{ col.label }}
  <TableFilter filter-name="Job title" :has-filter="jobsFilter.jobTitle && jobsFilter.jobTitle.length">
    <q-input filled borderless debounce="300" v-model="jobsFilter.jobTitle" placeholder="Job title">
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
  components: { TableFilter }
}
</script>
