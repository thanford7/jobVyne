<template>
  <q-select
    v-if="isLoaded"
    filled multiple clearable use-chips use-input
    :map-options="isEmitId" :emit-value="isEmitId"
    :options="states"
    @filter="filter"
    option-value="id"
    option-label="name"
    label="State"
  />
</template>

<script>
import { useAuthStore } from 'stores/auth-store.js'
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectJobState',
  props: {
    isEmitId: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      filterTxt: null
    }
  },
  computed: {
    states () {
      if (!this.isLoaded) {
        return
      }
      const states = this.employerStore.getJobStates(this.authStore.propUser.employer_id)
      if (!this.filterTxt || this.filterTxt === '') {
        return states
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return states.filter((s) => s.name.match(filterRegex))
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
