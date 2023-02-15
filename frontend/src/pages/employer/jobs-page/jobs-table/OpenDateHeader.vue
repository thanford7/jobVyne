<template>
  <!--  eslint-disable vue/no-mutating-props-->
  {{ col.label }}
  <TableFilter filter-name="Date range"
               :has-filter="jobsFilter.dateRange">
    <DateRangeSelector v-model="jobsFilter.dateRange" placeholder="Posted date" autofocus/>
  </TableFilter>
</template>

<script>
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import TableFilter from 'components/tables/TableFilter.vue'

export default {
  name: 'OpenDateHeader',
  props: {
    col: Object,
    jobsFilter: Object
  },
  components: { TableFilter, DateRangeSelector }
}
</script>
