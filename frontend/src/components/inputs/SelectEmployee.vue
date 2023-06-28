<template>
  <q-select
    v-if="isLoaded"
    filled use-chips use-input emit-value map-options
    :clearable="isMulti"
    :multiple="isMulti"
    :options="filteredEmployees"
    @filter="filter"
    option-value="id"
    :option-label="(employee) => `${employee.first_name} ${employee.last_name}`"
    label="Employee"
  />
</template>

<script>
import dataUtil from 'src/utils/data.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectEmployee',
  props: {
    employerId: [Number],
    isMulti: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      employerStore: null
    }
  },
  computed: {
    employees () {
      return dataUtil.sortBy(this.employerStore.getEmployees(this.employerId), 'first_name')
    },
    filteredEmployees () {
      if (!this.filterTxt || !this.filterTxt.length) {
        return this.employees
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.employees.filter((e) => {
        const { first_name: firstName, last_name: lastName } = e
        let isMatch = false
        if (firstName) {
          isMatch = firstName.match(filterRegex)
        }
        if (lastName) {
          isMatch = isMatch || lastName.match(filterRegex)
        }
        return isMatch
      })
    }
  },
  methods: {
    filter (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.employerStore = useEmployerStore()
    await this.employerStore.setEmployees(this.employerId)
    this.isLoaded = true
  }
}
</script>
