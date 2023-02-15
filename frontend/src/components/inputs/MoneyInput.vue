<template>
  <q-input
    v-if="isLoaded && selectedCurrency"
    filled :label="label" :mask="mask" unmasked-value
    :model-value="moneyValue"
    @update:model-value="updatePrice($event)"
    lazy-rules
    :rules="(isRequired) ? [
      (val) => val || 'This field is required'
    ] : null"
  >
    <template v-if="isIncludeCurrencySelection" v-slot:append>
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
import dataUtil from 'src/utils/data.js'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'MoneyInput',
  props: {
    moneyValue: {
      type: Number,
      default: 0
    },
    currencyName: {
      type: String,
      default: 'USD'
    },
    isIncludeCurrencySelection: {
      type: Boolean,
      default: true
    },
    isRequired: {
      type: Boolean,
      default: false
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
  watch: {
    moneyValue () {
      this.placeCursorEnd()
    }
  },
  computed: {
    mask () {
      let mask = `${this.selectedCurrency.symbol}`
      let digitsStr = ''
      if (dataUtil.isNil(this.moneyValue)) {
        digitsStr = '#'
      } else {
        for (let x = 0; x <= this.moneyValue.toString().length; x++) {
          if ((x - 1) % 3 || x < 3) {
            digitsStr = '#' + digitsStr
          } else {
            digitsStr = '#,' + digitsStr
          }
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
      this.$emit('update:moneyValue', parseFloat(price))
    },
    setCurrency (currency) {
      this.selectedCurrency = currency
      this.$emit('update:currencyName', currency.name)
    },
    placeCursorEnd () {
      const end = this.mask.length
      const input = this.$el.querySelector('input')
      input.setSelectionRange(end, end)
      input.focus()
    }
  },
  async mounted () {
    const globalStore = useGlobalStore()
    await globalStore.setCurrencies()
    this.currencies = globalStore.currencies
    this.selectedCurrency = this.currencies.find((c) => c.name === this.currencyName)
    this.isLoaded = true
  }
}
</script>
