<template>
  <q-select
    ref="select"
    :loading="isLoading"
    :multiple="isMulti"
    :use-chips="isMulti"
    filled emit-value map-options use-input
    :options="filteredJobLevels"
    option-value="id"
    option-label="name"
    :label="`${label}${(isMulti) ? 's' : ''}`"
    @filter="filterJobLevels"
    input-debounce="0"
    lazy-rules
    :rules="rules"
  />
</template>

<script>

import { useTaxonomyStore } from 'stores/taxonomy-store.js'

export default {
  name: 'SelectJobLevel',
  props: {
    isMulti: Boolean,
    isRequired: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Job level'
    }
  },
  data () {
    return {
      filterTxt: null,
      jobLevels: [],
      isLoading: false
    }
  },
  computed: {
    rules () {
      if (!this.isRequired) {
        return null
      }
      if (this.isMulti) {
        return [
          (val) => Boolean(val && val.length) || 'This field is required'
        ]
      }
      return [(val) => Boolean(val) || 'This field is required']
    },
    filteredJobLevels () {
      if (!this.filterTxt || !this.filterTxt.length) {
        return this.jobLevels
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.jobLevels.filter((jt) => jt.name.match(filterRegex))
    }
  },
  methods: {
    filterJobLevels (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.isLoading = true
    const taxStore = useTaxonomyStore()
    await taxStore.setJobLevels()
    this.jobLevels = taxStore.getJobLevels()
    this.isLoading = false
  }
}
</script>
