<template>
  <DialogBase
    ref="baseDialog"
    base-title-text="Job Filter"
    width="700px"
    primary-button-text="Filter jobs"
    :ok-fn="setEmitData"
    :is-submit-on-enter="true"
  >
    <q-form ref="form" class="row q-gutter-y-sm">
      <div class="col-12 col-md-4 q-pr-md-sm">
        <q-input
          v-model="filters.search_regex"
          filled
          :label="(isSingleEmployer) ? 'Job title' : 'Job title or Company'"
          debounce="500"
          @keyup.enter.prevent="$refs.baseDialog.onOkClick"
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
      <div class="col-12">
        <SelectJobProfession
          v-model="filters.job_profession_ids"
          :is-multi="true" :is-required="false"
        />
      </div>
    </q-form>
  </DialogBase>
</template>
<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import InputLocation from 'components/inputs/InputLocation.vue'
import MoneyInput from 'components/inputs/MoneyInput.vue'
import SelectJobProfession from 'components/inputs/SelectJobProfession.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import dataUtil from 'src/utils/data.js'

export default {
  name: 'DialogJobFilter',
  components: { SelectJobProfession, MoneyInput, SelectRemote, InputLocation, DialogBase },
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
