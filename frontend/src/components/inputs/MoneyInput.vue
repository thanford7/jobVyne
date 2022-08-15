<template>
  <q-input
    v-if="isLoaded"
    filled
    :label="label"
    :mask="mask"
    unmasked-value
    :model-value="modelValue"
    @update:model-value="updatePrice($event)"
  >
    <template v-slot:append>
      <q-btn-dropdown
        :label="`${selectedCurrency.symbol} ${selectedCurrency.name}`"
        class="h-100 border-left-1-gray-300" flat square style="margin-right: -12px;"
      >
        <q-list>
          <q-item
            v-for="currency in currencies"
            clickable v-close-popup @click="setCurrency(currency)"
          >
            <q-item-section>
              {{ currency.symbol }} {{ currency.name }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </template>
    <template v-slot:after>
      <slot name="after"/>
    </template>
  </q-input>
</template>

<script>
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'MoneyInput',
  props: {
    modelValue: {
      type: Number,
      default: 0
    },
    defaultCurrency: {
      type: String,
      default: 'USD'
    },
    precision: {
      type: Number,
      default: 0
    },
    label: String
  },
  data () {
    return {
      isLoaded: false,
      selectedCurrency: null,
      currencies: null
    }
  },
  computed: {
    mask () {
      let mask = `${this.selectedCurrency.symbol} `
      let digitsStr = ''
      for (let x = 0; x <= this.modelValue.toString().length; x++) {
        if ((x - 1) % 3 || x < 3) {
          digitsStr = '#' + digitsStr
        } else {
          digitsStr = '#,' + digitsStr
        }
      }
      mask += digitsStr
      if (this.precision > 0) {
        mask += '.' + '#'.repeat(this.precision)
      }
      return mask
    }
  },
  methods: {
    updatePrice (price) {
      if (!price || !price.toString().length) {
        price = 0
      }
      this.$emit('update:modelValue', parseFloat(price))
    },
    setCurrency (currency) {
      this.selectedCurrency = currency
      this.$emit('update-currency', currency)
    }
  },
  async mounted () {
    const globalStore = useGlobalStore()
    await globalStore.setCurrencies()
    this.currencies = globalStore.currencies
    this.setCurrency(this.currencies.find((c) => c.name === this.defaultCurrency))
    this.isLoaded = true
  }
}
</script>
