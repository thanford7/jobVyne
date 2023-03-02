<template>
  <q-select
    v-if="isLoaded"
    :multiple="isMulti"
    :use-chips="isMulti"
    filled emit-value map-options
    :options="this.employerStore.allEmployers"
    option-value="id"
    option-label="name"
    label="Employer"
  />
</template>

<script>
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectEmployer',
  props: {
    isMulti: Boolean
  },
  data () {
    return {
      isLoaded: false
    }
  },
  async mounted () {
    await this.employerStore.setAllEmployers()
    this.isLoaded = true
  },
  setup () {
    return {
      employerStore: useEmployerStore()
    }
  }
}
</script>
