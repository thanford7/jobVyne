<template>
  <input
    ref="inputRef"
    type="text"
  />
</template>

<script>
import { useCurrencyInput } from 'vue-currency-input'

export default {
  name: 'CurrencyInput',
  props: {
    modelValue: Number,
    options: Object
  },
  setup (props) {
    const { inputRef } = useCurrencyInput(props.options, true)
    return { inputRef }
  }
}
</script>
