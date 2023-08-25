<template>
  <q-select
    v-if="isLoaded"
    :multiple="isMulti"
    :use-chips="isMulti"
    filled emit-value map-options use-input
    @filter="filter"
    :options="filteredEmployers"
    option-value="id"
    option-label="employer_name"
    :label="`Employer${(isMulti) ? 's' : ''}`"
    lazy-rules
    :rules="rules"
  />
</template>

<script>
import { useEmployerStore } from 'stores/employer-store.js'

export default {
  name: 'SelectEmployer',
  props: {
    isMulti: Boolean,
    employers: [Array, null],
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isLoaded: false,
      allEmployers: null,
      filterTxt: null
    }
  },
  computed: {
    rules () {
      if (!this.isRequired) {
        return []
      } else if (this.isMulti) {
        return [
          (val) => (val && val.length) || 'The employer field is required'
        ]
      } else {
        return [
          (val) => val || 'The employer field is required'
        ]
      }
    },
    filteredEmployers () {
      if (!this.isLoaded) {
        return
      }
      if (!this.filterTxt || this.filterTxt === '') {
        return this.allEmployers
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.allEmployers.filter((e) => e.employer_name.match(filterRegex))
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
