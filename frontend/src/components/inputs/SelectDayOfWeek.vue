<template>
  <q-select
    filled emit-value map-options :use-chips="isMulti"
    :multiple="isMulti"
    :label="`Day${(isMulti) ? 's' : ''} of week`"
    :options="dowOptions"
    option-value="val"
    option-label="label"
    :model-value="modelValue"
    @update:model-value="emitVal($event)"
  >
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-select>
</template>

<script>
import { DAYS_OF_WEEK } from 'src/utils/datetime.js'

export default {
  inname: 'SelectDayOfWeek',
  props: {
    modelValue: [Number, Array, null],
    isMulti: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    dowOptions () {
      return Object.entries(DAYS_OF_WEEK).map(([dowNum, dowCfg]) => {
        return { val: parseInt(dowNum), label: dowCfg.name }
      })
    }
  },
  methods: {
    emitVal (val) {
      this.$emit('update:modelValue', val)
    },
    getDowBitsFromSelection (val) {
      if (Array.isArray(val)) {
        return val.reduce((allBits, dowNum) => {
          allBits |= DAYS_OF_WEEK[dowNum].dowBit
          return allBits
        }, 0)
      } else if (val) {
        return DAYS_OF_WEEK[val].dowBit
      }
      return 0
    }
  }
}
</script>
