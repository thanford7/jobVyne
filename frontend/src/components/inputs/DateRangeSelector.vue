<template>
  <q-input
    filled
    :clearable="isClearable"
    :model-value="dateRangeText"
    @click="$refs.dateRange.show()"
    @clear="clearRange"
    :label="placeholder"
    style="min-width: 300px;"
  >
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy ref="dateRange" cover transition-show="scale" transition-hide="scale">
          <q-date
            range minimal
            :model-value="dateRange"
            @update:model-value="$emit('update:model-value', getStandardizedValue($event))"
          />
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'

export default {
  name: 'DateRangeSelector',
  data () {
    return {
      dateRange: null
    }
  },
  props: {
    modelValue: [Object, null],
    placeholder: {
      type: String,
      default: 'Date'
    },
    isClearable: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    dateRangeText () {
      if (!this.dateRange) {
        return null
      }

      if (!dataUtil.isObject(this.dateRange)) {
        return dateTimeUtil.getShortDate(this.dateRange)
      }
      const { from, to } = this.dateRange
      if (from && !to) {
        return `${dateTimeUtil.getShortDate(from)} onwards`
      } else if (!from && to) {
        return `Up to ${dateTimeUtil.getShortDate(to)}`
      }
      return `${dateTimeUtil.getShortDate(from)} to ${dateTimeUtil.getShortDate(to)}`
    }
  },
  watch: {
    modelValue () {
      this.updateDateRange()
    }
  },
  methods: {
    getStandardizedValue (val) {
      // Make sure model is always in the form of {to: from: }
      if (!val || dataUtil.isObject(val)) {
        return val
      }
      return { to: val, from: val }
    },
    clearRange () {
      this.$emit('update:model-value', null)
    },
    updateDateRange () {
      // q-date requires a single value to be in string format so we convert back
      if (!this.modelValue) {
        this.dateRange = null
        return
      }
      const { to, from } = this.modelValue
      if (to === from) {
        this.dateRange = to
        return
      }
      this.dateRange = this.modelValue
    }
  },
  mounted () {
    this.updateDateRange()
  }
}
</script>
