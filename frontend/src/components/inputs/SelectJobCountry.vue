<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :options="countries"
    @filter="filter"
    option-value="id"
    option-label="name"
    label="Country"
  />
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectJobCountry',
  data () {
    return {
      isLoaded: false,
      filterTxt: null
    }
  },
  computed: {
    countries () {
      if (!this.isLoaded) {
        return
      }
      const countries = this.employerStore.getJobCountries(this.authStore.propUser.employer_id)
      if (!this.filterTxt || this.filterTxt === '') {
        return countries
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return countries.filter((c) => c.name.match(filterRegex))
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
    await this.employerStore.setEmployerJobs(this.authStore.propUser.employer_id)
    this.isLoaded = true
  }
}
</script>
