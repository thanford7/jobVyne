<template>
  <q-input
    :model-value="modelValue" @update:model-value="emitUpdate($event)"
    filled mask="time"
    :label="`Time of day (${dateTimeUtil.getCurrentTimeZone()})`"
    lazy-rules
    :rules="[
      (val) => !isRequired || val || 'Value is required',
      (val) => !val || /^([0-1]?\d|2[0-3]):[0-5]\d$/.test(val) || 'Must be a valid time'
    ]"
  >
    <template v-slot:append>
      <q-icon name="access_time" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-time :model-value="modelValue" @update:model-value="emitUpdate($event)" :minute-options="minuteOptions">
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat/>
            </div>
          </q-time>
        </q-popup-proxy>
      </q-icon>
    </template>
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-input>
</template>

<script>
import dateTimeUtil from 'src/utils/datetime.js'

export default {
  name: 'InputTime',
  props: {
    modelValue: String,
    isRequired: {
      type: Boolean,
      default: true
    },
    minuteOptions: {
      type: [Array, null],
      default: () => [0, 15, 30, 45]
    }
  },
  data () {
    return {
      dateTimeUtil
    }
  },
  methods: {
    emitUpdate (val) {
      this.$emit('update:modelValue', val)
    }
  }
}
</script>
