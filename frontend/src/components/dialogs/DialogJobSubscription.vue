<template>
  <DialogBase
    base-title-text="Edit job subscription"
    primary-button-text="Update"
    @ok="saveJobSubscription"
  >
    <q-form ref="form">
      <div class="row q-gutter-y-md q-mt-sm">
        <div class="col-12">
          <q-input
            v-model="formData.job_title_regex"
            filled label="Include job titles"
          >
            <template v-slot:after>
              <CustomTooltip>
                Use partial or full job titles. You can include multiple titles using a "|" separator
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <q-input
            v-model="formData.exclude_job_title_regex"
            filled label="Exclude job titles"
          >
            <template v-slot:after>
              <CustomTooltip>
                Use partial or full job titles. You can include multiple titles using a "|" separator
              </CustomTooltip>
            </template>
          </q-input>
        </div>
        <div class="col-12">
          <SelectEmployer v-model="formData.employers" :is-multi="true"/>
        </div>
        <div class="col-12">
          <SelectJobCity v-model="formData.cities" :is-emit-id="true" :is-all="true"/>
        </div>
        <div class="col-12">
          <SelectJobState v-model="formData.states" :is-emit-id="true" :is-all="true"/>
        </div>
        <div class="col-12">
          <SelectJobCountry v-model="formData.countries" :is-emit-id="true" :is-all="true"/>
        </div>
        <div class="col-12">
          <SelectRemote v-model="formData.remote_type_bit"/>
        </div>
      </div>
    </q-form>
  </DialogBase>
</template>

<script>
import DialogBase from 'components/dialogs/DialogBase.vue'
import SelectEmployer from 'components/inputs/SelectEmployer.vue'
import SelectJobCity from 'components/inputs/SelectJobCity.vue'
import SelectJobCountry from 'components/inputs/SelectJobCountry.vue'
import SelectJobState from 'components/inputs/SelectJobState.vue'
import SelectRemote from 'components/inputs/SelectRemote.vue'
import { getAjaxFormData } from 'src/utils/requests.js'

export default {
  name: 'DialogJobSubscription',
  extends: DialogBase,
  inheritAttrs: false,
  components: {
    DialogBase,
    SelectEmployer,
    SelectJobCity,
    SelectJobState,
    SelectJobCountry,
    SelectRemote
  },
  props: {
    jobSubscription: Object
  },
  data () {
    return {
      formData: {}
    }
  },
  methods: {
    async saveJobSubscription () {
      await this.$api.put(`employer/job-subscription/${this.jobSubscription.id}`, getAjaxFormData(this.formData))
      this.$emit('ok')
    }
  },
  mounted () {
    this.formData = Object.assign({}, this.jobSubscription.filters)

    // Turn filter objects into flat IDs
    const flattenFilterItems = ['cities', 'states', 'countries', 'jobs', 'employers']
    flattenFilterItems.forEach((filterKey) => {
      this.formData[filterKey] = this.formData[filterKey].map((item) => item.id)
    })
  }
}
</script>
