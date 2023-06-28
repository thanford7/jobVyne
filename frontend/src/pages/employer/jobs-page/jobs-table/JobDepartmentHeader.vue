<template>
<!--  eslint-disable vue/no-mutating-props-->
  {{ col.label }}
  <TableFilter filter-name="Job department"
               :has-filter="jobsFilter.departments && jobsFilter.departments.length">
    <SelectJobDepartment v-model="jobsFilter.departments" autofocus/>
  </TableFilter>
</template>

<script>
import SelectJobDepartment from 'components/inputs/SelectJobDepartment.vue'
import TableFilter from 'components/tables/TableFilter.vue'

export default {
  name: 'JobDepartmentHeader',
  props: {
    col: Object,
    jobsFilter: Object
  },
  components: { TableFilter, SelectJobDepartment }
}
</script>
