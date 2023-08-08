<template>
  <q-select
    ref="select"
    :loading="isLoading"
    :multiple="isMulti"
    :use-chips="isMulti"
    filled emit-value map-options use-input
    :options="filteredJobProfessions"
    option-value="id"
    option-label="name"
    :label="`${label}${(isMulti) ? 's' : ''}`"
    @filter="filterProfessions"
    input-debounce="0"
    lazy-rules
    :rules="rules"
  >
  </q-select>
</template>

<script>

import { useTaxonomyStore } from 'stores/taxonomy-store.js'

export default {
  name: 'SelectJobProfession',
  props: {
    isMulti: Boolean,
    isRequired: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Job profession'
    }
  },
  data () {
    return {
      filterTxt: null,
      jobProfessions: [],
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
    filteredJobProfessions () {
      if (!this.filterTxt || !this.filterTxt.length) {
        return this.jobProfessions
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return this.jobProfessions.filter((jt) => jt.name.match(filterRegex))
    }
  },
  methods: {
    filterProfessions (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  },
  async mounted () {
    this.isLoading = true
    const taxStore = useTaxonomyStore()
    await taxStore.setJobProfessions()
    this.jobProfessions = taxStore.getJobProfessions()
    this.isLoading = false
  }
}
</script>
