<template>
  <!--  eslint-disable vue/no-mutating-props-->
  {{ col.label }}
  <TableFilter
    filter-name="Location"
    :has-filter="(
      (jobsFilter.cities && jobsFilter.cities.length) ||
      (jobsFilter.states && jobsFilter.states.length) ||
      (jobsFilter.countries && jobsFilter.countries.length)
    )"
  >
    <div class="q-gutter-y-sm">
      <SelectJobCity v-model="jobsFilter.cities"/>
      <SelectJobState v-model="jobsFilter.states"/>
      <SelectJobCountry v-model="jobsFilter.countries"/>
    </div>
  </TableFilter>
</template>

<script>
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import TableFilter from 'components/tables/TableFilter.vue'

export default {
  name: 'LocationsHeader',
  props: {
    col: Object,
    jobsFilter: Object
  },
  components: { TableFilter, SelectJobCity, SelectJobState, SelectJobCountry }
}
</script>
