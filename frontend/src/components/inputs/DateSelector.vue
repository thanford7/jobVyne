<template>
  <q-input
    :model-value="modelValue"
    @update:model-value="$emit('update:model-value', $event)"
    filled :label="formattedLabel" mask="##/##/####"
    lazy-rules :rules="rules"
  >
    <template v-slot:append>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-date
            :model-value="modelValue"
            @update:model-value="$emit('update:model-value', $event)"
            :mask="dateTimeUtil.serializeDateFormat"
          >
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import dateTimeUtil from 'src/utils/datetime.js'

export default {
  name: 'DateSelector',
  props: {
    modelValue: [null, String],
    label: {
      type: String,
      default: 'Date'
    },
    isRequired: {
      type: Boolean,
      default: false
    },
    additionalRules: {
      type: [Array, null]
    }
  },
  data () {
    return {
      dateTimeUtil
    }
  },
  computed: {
    formattedLabel () {
      return `${this.label} (${dateTimeUtil.serializeDateFormat})`
    },
    rules () {
      const rules = []
      if (this.isRequired) {
        rules.push((val) => (val && val.length) || 'This field is required')
      }
      return [...rules, ...(this.additionalRules || [])]
    }
  }
}
</script>
