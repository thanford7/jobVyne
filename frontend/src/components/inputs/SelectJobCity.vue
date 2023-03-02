<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :map-options="isEmitId" :emit-value="isEmitId"
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
import { useJobStore } from 'stores/job-store.js'

export default {
  name: 'SelectJobCity',
  props: {
    isEmitId: {
      type: Boolean,
      default: false
    },
    employerId: {
      type: [String, Number, null]
    },
    isAll: { // Ignore employer and get all job departments
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null,
      authStore: null,
      employerStore: null,
      jobStore: null
    }
  },
  computed: {
    cities () {
      if (!this.isLoaded) {
        return
      }
      let cities = []
      if (this.isAll) {
        cities = this.jobStore.getCities()
      } else {
        cities = this.employerStore.getJobCities(this.employerId || this.authStore.propUser.employer_id)
      }
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
    this.jobStore = useJobStore()
    await this.authStore.setUser()
    const employerId = this.employerId || this.authStore.propUser.employer_id
    if (this.isAll) {
      await this.jobStore.setLocations()
    } else {
      await this.employerStore.setEmployerJobs(employerId)
    }
    this.isLoaded = true
  },
  beforeUnmount () {
    this.$emit('before-unmount')
  }
}
</script>
