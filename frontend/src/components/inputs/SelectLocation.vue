<template>
  <q-select
    ref="select"
    :multiple="isMulti"
    filled emit-value map-options use-chips use-input
    :options="formattedLocations"
    option-value="id"
    option-label="fullLocationText"
    :label="`Location${(isMulti) ? 's' : ''}`"
    :new-value-mode="(isAllowCreate) ? 'add-unique' : null"
    @filter="filterLocations"
    input-debounce="0"
    @new-value="createLocation"
    lazy-rules
    :rules="(isRequired) ? [
      (val) => (val && val.length) || 'This field is required'
    ] : null"
  >
    <template v-if="isAllowCreate" v-slot:no-option="{ inputValue }">
      <q-item clickable @click="createLocation(inputValue)">
        <q-item-section>
          Create "{{ inputValue }}" location
        </q-item-section>
      </q-item>
    </template>
    <template v-if="isAllowCreate" v-slot:after>
      <CustomTooltip>
        Start typing to filter and/or create a new location. To create a remote
        location, include "Remote" in the location text.
      </CustomTooltip>
    </template>
  </q-select>
</template>

<script>
import CustomTooltip from 'components/CustomTooltip.vue'
import locationUtil from 'src/utils/location.js'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'SelectLocation',
  components: { CustomTooltip },
  props: {
    isMulti: Boolean,
    locations: Array,
    isAllowCreate: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      filterTxt: null,
      locationUtil
    }
  },
  computed: {
    formattedLocations () {
      const formattedLocations = locationUtil.updateFullLocations(this.locations)
      dataUtil.sortBy(formattedLocations, 'fullLocationText', true)
      if (!this.filterTxt || this.filterTxt === '') {
        return formattedLocations
      }
      const filterRegex = new RegExp(`.*?${this.filterTxt}.*?`, 'i')
      return formattedLocations.filter((l) => l.fullLocationText.match(filterRegex))
    }
  },
  methods: {
    createLocation (locationText) {
      const newLocation = { id: locationText, fullLocationText: locationText }
      this.filterTxt = null
      this.$refs.select.updateInputValue('')
      const newVal = (this.isMulti) ? [...dataUtil.getForceArray(this.$refs.select.modelValue), newLocation.id] : newLocation.id
      this.$refs.select.$emit('update:modelValue', newVal)
      this.$refs.select.blur()
    },
    filterLocations (filterTxt, update) {
      update(() => {
        this.filterTxt = filterTxt
      })
    }
  }
}
</script>
