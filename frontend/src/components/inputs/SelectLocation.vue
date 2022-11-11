<template>
  <q-select
    :multiple="isMulti"
    filled emit-value map-options use-chips use-input
    :options="formattedLocations"
    option-value="id"
    option-label="fullLocationText"
    label="Location"
    @filter="filterLocations"
  />
</template>

<script>
import locationUtil from 'src/utils/location.js'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'SelectLocation',
  props: {
    isMulti: Boolean,
    locations: Array
  },
  data () {
    return {
      filterTxt: null,
      locationUtil
    }
  },
  computed: {
    formattedLocations () {
      const formattedLocations = this.locations.reduce((formattedLocations, location) => {
        location.fullLocationText = locationUtil.getFullLocation(location)
        formattedLocations.push(location)
        return formattedLocations
      }, [])
      dataUtil.sortBy(formattedLocations, 'fullLocationText', true)
      if (!this.filterTxt || this.filterTxt === '') {
        return formattedLocations
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return formattedLocations.filter((l) => l.fullLocationText.match(filterRegex))
    }
  },
  methods: {
    filterLocations (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  }
}
</script>
