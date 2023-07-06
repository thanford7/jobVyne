<template>
  <q-select
    ref="select"
    :loading="isLoading"
    :multiple="isMulti"
    filled emit-value map-options use-chips use-input
    :options="filteredJobTitles"
    option-value="id"
    option-label="name"
    :label="`Job title${(isMulti) ? 's' : ''}`"
    @filter="filterTitles"
    input-debounce="0"
    lazy-rules
    :rules="(isRequired) ? [
      (val) => (val && val.length) || 'This field is required'
    ] : null"
  >
  </q-select>
</template>

<script>

import { useTaxonomyStore } from 'stores/taxonomy-store.js'

export default {
  name: 'SelectJobTitle',
  props: {
    isMulti: Boolean,
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      filterTxt: null,
      jobTitles: [],
      isLoading: false
    }
  },
  computed: {
    filteredJobTitles () {
      if (!this.filterTxt || !this.filterTxt.length) {
        return this.jobTitles
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.jobTitles.filter((jt) => jt.name.match(filterRegex))
    }
  },
  methods: {
    filterTitles (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.isLoading = true
    const taxStore = useTaxonomyStore()
    await taxStore.setJobTitles()
    this.jobTitles = taxStore.getJobTitles()
    this.isLoading = false
  }
}
</script>
