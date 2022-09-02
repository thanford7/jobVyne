<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input emit-value map-options
    :options="filteredEmployees"
    @filter="filter"
    option-value="id"
    :option-label="(employee) => `${employee.first_name} ${employee.last_name}`"
    label="Employee"
  />
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectEmployee',
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      authStore: null,
      employerStore: null
    }
  },
  computed: {
    employees () {
      return this.employerStore.getEmployees(this.authStore.propUser.employer_id)
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
    this.authStore = useAuthStore()
    this.employerStore = useEmployerStore()
    await this.authStore.setUser()
    await this.employerStore.setEmployees(this.authStore.propUser.employer_id)
    this.isLoaded = true
  }
}
</script>
