<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :options="departments"
    @filter="filter"
    option-value="id"
    option-label="name"
    label="Department"
  />
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectJobDepartment',
  data () {
    return {
      isLoaded: false,
      filterTxt: null
    }
  },
  computed: {
    departments () {
      if (!this.isLoaded) {
        return
      }
      const departments = this.employerStore.getJobDepartments(this.authStore.propUser.employer_id)
      if (!this.filterTxt || this.filterTxt === '') {
        return departments
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return departments.filter((d) => d.name.match(filterRegex))
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
  },
  beforeUnmount () {
    this.$emit('before-unmount')
  }
}
</script>
