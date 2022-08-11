<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :options="cities"
    @filter="filter"
    option-value="id"
    option-label="name"
    label="City"
  />
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectJobCity',
  data () {
    return {
      isLoaded: false,
      filterTxt: null
    }
  },
  computed: {
    cities () {
      if (!this.isLoaded) {
        return
      }
      const cities = this.employerStore.getJobCities(this.authStore.propUser.employer_id)
      if (!this.filterTxt || this.filterTxt === '') {
        return cities
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return cities.filter((c) => c.match(filterRegex))
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
