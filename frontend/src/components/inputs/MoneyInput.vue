<template>
  <q-field
    v-if="isLoaded && selectedCurrency"
    filled
    :model-value="moneyValue"
    :label="label"
  >
    <template v-slot:control="{ id, modelValue, floatingLabel }">
      <CurrencyInput
        :id="id" class="q-field__input"
        :model-value="modelValue"
        @change="emitMoneyVal($event)"
        :options="moneyFormat"
        v-show="floatingLabel"
      />
    </template>
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
  </q-field>
</template>

<script>

import CurrencyInput from 'components/inputs/CurrencyInput.vue'
import { useGlobalStore } from 'stores/global-store.js'

export default {
  name: 'MoneyInput2',
  props: {
    moneyValue: [Number, null],
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
  components: { CurrencyInput },
  data () {
    return {
      isLoaded: false,
      selectedCurrency: null,
      currencies: null,
      moneyFormat: {
        currency: this.currencyName,
        precision: this.precision
      }
    }
  },
  methods: {
    emitMoneyVal (val) {
      if (isNaN(val)) {
        return
      }
      this.$emit('update:moneyValue', val)
    },
    setCurrency (currency) {
      this.selectedCurrency = currency
      this.moneyFormat = { currency: currency.name }
      this.$emit('update:currencyName', currency.name)
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
