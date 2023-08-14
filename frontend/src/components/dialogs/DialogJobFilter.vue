<template>
  <DialogBase
    base-title-text="Job Filter"
    width="700px"
    primary-button-text="Filter jobs"
    :ok-fn="setEmitData"
  >
    <q-form ref="form" class="row q-gutter-y-sm">
      <div class="col-12 col-md-4 q-pr-md-sm">
        <q-input
          v-model="filters.search_regex"
          filled
          :label="(isSingleEmployer) ? 'Job title' : 'Job title or Company'"
          debounce="500"
        >
          <template v-slot:append>
            <q-icon name="search"/>
          </template>
        </q-input>
      </div>
      <div class="col-12 col-md-8 q-pl-md-sm">
        <InputLocation
          v-model:location="filters.location"
          v-model:range_miles="filters.range_miles"
          :is-include-range="true"
        />
      </div>
      <div class="col-12 col-md-4 q-pr-md-sm">
        <SelectRemote v-model="filters.remote_type_bit"/>
      </div>
      <div class="col-12 col-md-4 q-pl-md-sm">
        <MoneyInput
          v-model:money-value.number="filters.minimum_salary"
          v-model:currency-name="filters.currency"
          :is-include-currency-selection="false"
          label="Minimum salary"
        />
      </div>
    </q-form>
  </DialogBase>
</template>
<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DialogJobFilter',
  components: { MoneyInput, SelectRemote, InputLocation, DialogBase },
  props: {
    jobFilters: Object,
    isSingleEmployer: Boolean
  },
  data () {
    return {
      filters: {}
    }
  },
  methods: {
    async setEmitData () {
      return this.filters
    }
  },
  mounted () {
    this.filters = dataUtil.deepCopy(this.jobFilters)
  }
}
</script>
