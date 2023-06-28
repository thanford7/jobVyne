<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :map-options="isEmitId" :emit-value="isEmitId"
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
import { useJobStore } from 'stores/job-store.js'

export default {
  name: 'SelectJobCountry',
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
    countries () {
      if (!this.isLoaded) {
        return
      }
      let countries = []
      if (this.isAll) {
        countries = this.jobStore.getCountries()
      } else {
        countries = this.employerStore.getJobCountries(this.employerId || this.authStore.propUser.employer_id)
      }
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
