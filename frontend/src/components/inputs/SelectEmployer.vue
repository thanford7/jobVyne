<template>
  <q-select
    v-if="isLoaded"
    :multiple="isMulti"
    :use-chips="isMulti"
    filled emit-value map-options use-input
    @filter="filter"
    :options="filteredEmployers"
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
    isMulti: Boolean,
    employers: [Array, null]
  },
  data () {
    return {
      isLoaded: false,
      allEmployers: null,
      filterTxt: null
    }
  },
  computed: {
    filteredEmployers () {
      if (!this.isLoaded) {
        return
      }
      if (!this.filterTxt || this.filterTxt === '') {
        return this.allEmployers
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.allEmployers.filter((e) => e.name.match(filterRegex))
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
    if (this.employers) {
      this.allEmployers = this.employers
    } else {
      await this.employerStore.setAllEmployers()
      this.allEmployers = this.employerStore.allEmployers
    }
    this.isLoaded = true
  },
  setup () {
    return {
      employerStore: useEmployerStore()
    }
  }
}
</script>
