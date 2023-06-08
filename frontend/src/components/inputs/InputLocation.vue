<template>
  <div
    class="grid-container"
    :class="{
      'grid-container__range': isAllowRange,
      'grid-container__mobile': utilStore.isMobile
    }"
  >
    <q-select
      ref="select"
      label="Location or Zip Code"
      :model-value="location"
      @update:model-value="emitLocation"
      filled use-input clearable :multiple="isMulti" :use-chips="isMulti"
      :hide-dropdown-icon="true"
      :loading="isLoading"
      @input-value="getLocationsDebounceFn"
      new-value-mode="add-unique"
      :options="locationOptions"
      option-label="text"
      option-value="text"
    >
      <template v-slot:selected-item="scope">
        <q-chip v-if="isMulti" clickable removable>
          <span class="ellipsis" :title="scope.opt.text">{{ scope.opt.text }}</span>
        </q-chip>
        <span v-else class="ellipsis" :title="scope.opt.text">{{ scope.opt.text }}</span>
      </template>
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
    <q-select
      v-if="isAllowRange"
      :model-value="range_miles"
      @update:model-value="$emit('update:range_miles', $event)"
      filled map-options emit-value
      label="Within distance"
      :options="[{ val: 10 }, { val: 25 }, { val: 50 }, { val: 100 }]"
      :option-label="(dist) => `${dist.val} miles`"
      option-value="val"
      :class="(utilStore.isMobile) ? 'q-mt-sm' : 'q-ml-sm'"
    />
  </div>
</template>

<script>
import { debounce } from 'quasar'
import { useUtilStore } from 'stores/utility-store.js'

export default {
  name: 'InputLocation',
  props: {
    location: [Object, Array, null],
    range_miles: [Number, null],
    isIncludeRange: {
      type: Boolean,
      default: false
    },
    isMulti: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isAllowRange () {
      let hasCity = false
      if (this.isMulti && this.location) {
        hasCity = this.location.reduce((hasCity, location) => {
          hasCity = hasCity || Boolean(location.city)
          return hasCity
        }, false)
      } else if (!this.isMulti) {
        hasCity = this.location?.city
      }
      return hasCity && this.isIncludeRange
    }
  },
  data () {
    return {
      isLoading: false,
      locationOptions: [],
      getLocationsDebounceFn: null,
      utilStore: useUtilStore()
    }
  },
  methods: {
    emitLocation (location) {
      this.$emit('update:location', location)
      this.$refs.select.updateInputValue('')
    },
    async getLocationOptions (searchText) {
      if (!searchText || !searchText.length) {
        return
      }
      this.isLoading = true
      const resp = await this.$api.get('search/location/', {
        params: { search_text: searchText }
      })
      this.locationOptions = resp.data
      this.isLoading = false
      this.$refs.select.refresh()
      this.$refs.select.showPopup()
    }
  },
  created () {
    // Using debounce in methods is problematic
    // See: https://stackoverflow.com/questions/42199956/how-to-implement-debounce-in-vue2/49780382#49780382
    this.getLocationsDebounceFn = debounce(this.getLocationOptions, 700)
  }
}
</script>

<style scoped lang="scss">
.grid-container {
  display: grid;
  grid-template-columns: 1fr;

  &.grid-container__range:not(.grid-container__mobile) {
    grid-template-columns: 60% 40%;
  }
}
</style>
