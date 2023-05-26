<template>
  <q-select
    ref="select"
    label="Location or Zip Code"
    filled use-input
    :hide-dropdown-icon="true"
    :input-debounce="700"
    :loading="isLoading"
    @input-value="getLocationsDebounceFn"
    :options="locations"
    option-label="formatted_address"
    option-value="formatted_address"
  >
    <template v-slot:append>
      <q-icon name="place"/>
    </template>
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">
          Begin typing...
        </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import { debounce } from 'quasar'

export default {
  name: 'InputLocation',
  data () {
    return {
      isLoading: false,
      locations: [],
      getLocationsDebounceFn: null
    }
  },
  methods: {
    async getLocations (searchText) {
      this.isLoading = true
      if (!searchText || !searchText.length) {
        return
      }
      const resp = await this.$api.get('search/location/', {
        params: { search_text: searchText }
      })
      this.locations = resp.data
      this.isLoading = false
      this.$refs.select.refresh()
      this.$refs.select.showPopup()
    }
  },
  created () {
    // Using debounce in methods is problematic
    // See: https://stackoverflow.com/questions/42199956/how-to-implement-debounce-in-vue2/49780382#49780382
    this.getLocationsDebounceFn = debounce(this.getLocations, 700)
  }
}
</script>
